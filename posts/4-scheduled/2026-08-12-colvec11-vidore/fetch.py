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
"""Evidence for the ColVec1.1 post. Run from the repo root:

    uv run posts/2-drafting/colvec11-vidore/fetch.py

`ViDoRe(v3)` is visual document retrieval: page images ranked against text queries, rather
than text against text. Ten tasks. It is a much smaller field than the text boards — 41
models with complete coverage against 180 on `MTEB(eng, v2)` — which is why every rank
this post states carries "of 41". A rank among specialists who chose to enter is not the
same kind of claim as a rank among everyone.

Two generations of the same family are on the board, so the post can make a within-lab
comparison: same team, same two size classes, before and after. That comparison is immune
to the submission bias that shapes every cross-model ranking here, which is why it carries
more weight than the rank does.

Total parameters, not active: `activeParamsB` is unreliable on this API (see
docs/mteb-data.md) and total is what a reader means by model size.
"""

import json
import pathlib
import urllib.parse
import urllib.request
from datetime import date

from mtebpost.cards import write_card_data

API = "https://mteb-leaderboard-backend.hf.space"
BENCHMARK = "ViDoRe(v3)"
SUBJECTS = ("webAI-Official/webAI-ColVec1.1-8b", "webAI-Official/webAI-ColVec1.1-4b")
PRIOR = ("webAI-Official/webAI-ColVec1-9b", "webAI-Official/webAI-ColVec1-4b")
HERE = pathlib.Path(__file__).parent


def main() -> None:
    url = f"{API}/v1/benchmarks/{urllib.parse.quote(BENCHMARK)}/scores"
    with urllib.request.urlopen(url, timeout=180) as r:
        payload = json.load(r)

    tasks = payload["tasks"]
    rows = [r for r in payload["rows"]
            if all(r["scoresByTask"].get(t) is not None for t in tasks)]
    rows.sort(key=lambda r: -r["meanTask"])

    ranking = [
        {"rank": i, "model": r["model"]["name"],
         "score": round(r["meanTask"] * 100, 2),
         "params_b": r["model"].get("totalParamsB"),
         "released": r["model"].get("releaseDate")}
        for i, r in enumerate(rows, 1)
    ]
    by_name = {e["model"]: e for e in ranking}
    missing = [m for m in SUBJECTS + PRIOR if m not in by_name]
    if missing:
        raise SystemExit(f"not on {BENCHMARK} with complete coverage: {missing}")

    evidence = {
        "generated": date.today().isoformat(),
        "source": f"{API}/v1/benchmarks/.../scores",
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "tasks": sorted(tasks),
        "rule": f"complete coverage of all {len(tasks)} tasks",
        "n_complete": len(ranking),
        "subjects": [by_name[m] for m in SUBJECTS],
        "prior_generation": [by_name[m] for m in PRIOR],
        # The nearest competitor decides whether "1st" is a gap or a photo finish, so it
        # belongs in the evidence rather than only in the card.
        "runner_up": ranking[1],
        "top10": ranking[:10],
        "ranking": ranking,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # The card shows the top 10 rather than skipping rank 4-5 to jump straight from the
    # subjects to the prior generation — rank 2, 4 and 5 are the real competition, and
    # cutting them would make the generational jump look like the only story on the board.
    top10 = ranking[:10]
    write_card_data(HERE / "card.html", {
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "n_models": len(ranking),
        "rows": [
            {"model": e["model"], "score": e["score"], "params": e["params_b"],
             **({"subject": True} if e["model"] in SUBJECTS else {}),
             **({"prior": True} if e["model"] in PRIOR else {})}
            for e in top10
        ],
    })

    print(f"{BENCHMARK} — {len(payload['rows'])} rows, {len(ranking)} with all "
          f"{len(tasks)} tasks\n")
    for m in SUBJECTS + PRIOR:
        e = by_name[m]
        print(f"  rank {e['rank']:>2} of {len(ranking)}   {e['score']:>6}   "
              f"{e['params_b']}B   {m}")
    print(f"\n  runner-up: rank {ranking[1]['rank']} {ranking[1]['model']} "
          f"at {ranking[1]['score']}")


if __name__ == "__main__":
    main()
