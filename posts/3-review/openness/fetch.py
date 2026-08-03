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
"""Evidence for the openness post. Run from the repo root:

    uv run posts/3-review/openness/fetch.py

Uses `MTEB(Multilingual, v2)`, the default general-purpose benchmark. An earlier version
used `MTEB(eng, v2)` for a purely mechanical reason — 41 tasks loaded faster than 131 —
which stopped being true (load cost scales with model count, not task count) and stopped
mattering once the leaderboard API made either about a second. A claim about "the field"
made on the English set is really a claim about English.

Reads the API rather than the `mteb` package: ~2 s against ~15 min, same scores
(validated against `Benchmark.get_score()`), and better coverage — results that fail the
package's revision validation still appear, and those omissions are not random.

Three tiers, from `ModelMeta.openness`:

  proprietary   no open weights
  open weights  weights published, but not both training code and training data
  open source   weights + training code + training data — reproducible end to end

The tiers flatten a six-field record (weights, licence, code, data, paper, model card).
"Open source" here means specifically that someone else could rebuild the model, which is
the distinction that disappears when people say "open".
"""

import json
import pathlib
import urllib.parse
import urllib.request
from datetime import date

from mtebpost.cards import write_card_data

API = "https://mteb-leaderboard-backend.hf.space"
BENCHMARK = "MTEB(Multilingual, v2)"
TIERS = ("proprietary", "open weights", "open source")
HERE = pathlib.Path(__file__).parent


def tier_of(model: dict) -> str:
    o = model.get("openness") or {}
    if not model.get("openWeights"):
        return "proprietary"
    if o.get("open training code") and o.get("open training data"):
        return "open source"
    return "open weights"


def main() -> None:
    url = f"{API}/v1/benchmarks/{urllib.parse.quote(BENCHMARK)}/scores"
    with urllib.request.urlopen(url, timeout=180) as r:
        payload = json.load(r)

    tasks = set(payload["tasks"])
    counted = {t: 0 for t in TIERS}      # any results on this benchmark
    complete = {t: [] for t in TIERS}    # all tasks

    for row in payload["rows"]:
        m = row["model"]
        t = tier_of(m)
        counted[t] += 1
        if len(set(row["scoresByTask"]) & tasks) != len(tasks):
            continue  # a mean over a subset is not comparable to a mean over all of them
        complete[t].append({
            "model": m["name"],
            "score": round(row["meanTask"] * 100, 2),
            "openness_score": m.get("opennessScore"),
            "license": m.get("license"),
            "released": m.get("releaseDate"),
        })

    for t in TIERS:
        complete[t].sort(key=lambda r: -r["score"])

    evidence = {
        "generated": date.today().isoformat(),
        "source": f"{API}/v1/benchmarks/.../scores",
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "rule": f"complete coverage of all {len(tasks)} tasks",
        "tier_rule": {
            "proprietary": "openWeights is false",
            "open weights": "weights published, but not both training code and data",
            "open source": "weights + training code + training data",
        },
        "coverage": {t: {"any_results": counted[t], "complete_results": len(complete[t])}
                     for t in TIERS},
        "models": {t: complete[t] for t in TIERS},
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    total = sum(len(complete[t]) for t in TIERS)
    write_card_data(HERE / "card.html", {
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "n_models": total,
        "tiers": [
            {"tier": t, "n": len(complete[t]), "any": counted[t],
             "best": complete[t][0]["model"] if complete[t] else None,
             "best_score": complete[t][0]["score"] if complete[t] else None,
             "scores": [m["score"] for m in complete[t]]}
            for t in TIERS
        ],
    })

    print(f"{BENCHMARK} — {len(payload['rows'])} rows, {total} with all {len(tasks)} tasks\n")
    print(f"{'tier':<14}{'any':>6}{'complete':>10}{'best':>8}  top model")
    for t in TIERS:
        b = complete[t][0] if complete[t] else None
        print(f"{t:<14}{counted[t]:>6}{len(complete[t]):>10}"
              f"{(b['score'] if b else 0):>8}  {b['model'] if b else '-'}")


if __name__ == "__main__":
    main()
