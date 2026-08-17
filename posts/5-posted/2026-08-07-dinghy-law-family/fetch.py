#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
#
# [tool.uv]
# exclude-newer = "2026-08-01T00:00:00Z"
# ///
"""Evidence for the dinghy-law post. Run from the repo root:

    uv run posts/2-drafting/dinghy-law-family/fetch.py

**This one uses the leaderboard API rather than the `mteb` package**, and takes about a
second instead of about fourteen minutes. The reasons, and the one thing to watch:

* `import mteb` alone costs ~190 s and `load_results` ~4.5 s per model, so the 152-model
  Law cohort is a ~15-minute job locally. The same query against
  `mteb-leaderboard-backend.hf.space` returns in under a second with no heavy
  dependencies at all.
* The API is *more complete*. `voyageai/voyage-law-2` — the best-known legal embedding
  model — has all 8 Law task files on disk but its results sit under revisions `1` and
  `no_revision_available` and do not survive `load_results`' revision validation. The
  API includes it, at 65.39. A post about legal models that silently omitted the most
  famous legal model would be flattery by omission.
* Scores were validated against a local `Benchmark.get_score()` run: eight models across
  two benchmarks, exact matches to the last decimal.

**This post deliberately uses total parameters, not active.** The API's `activeParamsB`
currently returns total (see `issue.md` — it does not subtract the embedding table), so
active is unusable from this source until that lands. Total is also the more natural
axis for the claim being made here, which is "a small legal model beats a large general
one", not a claim about inference cost. If the fix ships, revisit — but do not
switch to active without checking the field again.

The cohort is every model with complete coverage of all 8 Law tasks. No size or language
filter: the benchmark itself is the filter, and the question is who is on the board.
"""

import json
import pathlib
import urllib.parse
import urllib.request
from datetime import date

from mtebpost.cards import write_card_data

API = "https://mteb-leaderboard-backend.hf.space"
BENCHMARK = "MTEB(Law, v1)"
SUBJECTS = ["Hanno-Labs/dinghy-law-4b-v1", "Hanno-Labs/dinghy-law-0.6b-v1"]

# Legal-domain models, identified by the model name declaring a legal domain.
#
# That is the strongest signal available, not a shortcut: none of these five declares a
# legal training dataset in its metadata and three list no training data at all, so there
# is no flag to prefer. Note the converse — `codefuse-ai/F2LLM-v2-14B` is a generalist
# that *does* list a legal dataset (Lawzhidao, one of 152). The line is "built for the
# domain", not "has seen the domain".
#
# Kept here rather than in prose so it is inspectable and a wrong entry shows in a diff.
LEGAL_DOMAIN = {
    "Hanno-Labs/dinghy-law-4b-v1",
    "Hanno-Labs/dinghy-law-0.6b-v1",
    "Mira190/Euler-Legal-Embedding-V1",
    "minetta/nemotron-3-embed-8b-legal",
    "voyageai/voyage-law-2",
}

HERE = pathlib.Path(__file__).parent
TOP_N = 8   # 8 rows fit the square card; enough to show the break at rank 6


def fetch_scores(benchmark: str) -> dict:
    url = f"{API}/v1/benchmarks/{urllib.parse.quote(benchmark)}/scores"
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def main() -> None:
    payload = fetch_scores(BENCHMARK)
    tasks = set(payload["tasks"])
    rows = []
    for r in payload["rows"]:
        m = r["model"]
        # complete coverage only: a mean over a subset is not comparable to a mean
        # over all 8, and the API returns partially-evaluated models too
        if len(set(r["scoresByTask"]) & tasks) != len(tasks):
            continue
        rows.append({
            "model": m["name"],
            "score": round(r["meanTask"] * 100, 2),
            "total_params_b": m["totalParamsB"],
            "released": m["releaseDate"],
            "open_weights": m["openWeights"],
            "legal_domain": m["name"] in LEGAL_DOMAIN,
        })
    rows.sort(key=lambda r: -r["score"])

    legal_ranks = [i for i, r in enumerate(rows, 1) if r["legal_domain"]]
    first_general = next(i for i, r in enumerate(rows, 1) if not r["legal_domain"])

    evidence = {
        "generated": date.today().isoformat(),
        "source": f"{API}/v1/benchmarks/.../scores",
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "rule": "complete coverage of all 8 Law tasks",
        "params_note": "total parameters; the API's activeParamsB currently returns total (see issue.md)",
        "legal_domain_list": sorted(LEGAL_DOMAIN),
        "legal_ranks": legal_ranks,
        "first_general_rank": first_general,
        "rows": rows,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    top = rows[:TOP_N]
    write_card_data(HERE / "card-1-dinghy-law-family.html", {
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "n_models": len(rows),
        "first_general_rank": first_general,
        "rows": [
            {"model": r["model"], "score": r["score"], "params": r["total_params_b"],
             **({"proprietary": True} if not r["open_weights"] else {}),
             **({"legal": True} if r["legal_domain"] else {}),
             **({"subject": True} if r["model"] in SUBJECTS else {})}
            for r in top
        ],
    })

    print(f"{len(payload['rows'])} rows from the API; {len(rows)} with all {len(tasks)} tasks")
    print(f"legal-domain models at ranks: {legal_ranks}")
    print(f"first general-purpose model at rank {first_general}\n")
    for i, r in enumerate(top, 1):
        tag = " [legal]" if r["legal_domain"] else ""
        print(f"  {i:>2}. {r['score']:>6}  {r['total_params_b'] or '?':>7}B  {r['model']}{tag}")


if __name__ == "__main__":
    main()
