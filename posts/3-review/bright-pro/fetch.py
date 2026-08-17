#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the BRIGHT-Pro benchmark_addition post. Run from the repo root:

    uv run posts/2-drafting/bright-pro/fetch.py

BRIGHT-Pro (mteb#4929) is a new registered benchmark — 7 StackExchange-domain retrieval
tasks (biology, earth science, economics, psychology, robotics, stackoverflow,
sustainable living), extending BRIGHT with per-query "aspect" annotations for
reasoning-intensive, agentic-search retrieval: each query's gold answer cites passages
covering several distinct reasoning aspects, so a retriever is scored on surfacing an
aspect-diverse evidence set rather than one relevant passage.

results#644 (same day, same author) submitted day-one results for 19 models, all with
complete 7-task coverage — unusual for a brand-new benchmark, and the reason this is a
`benchmark_addition` post with an actual leaderboard rather than just an announcement.

No single model is "the subject" here — this queries the whole benchmark and uses
`bars_card_data` with an empty subject list, same builder colvec11-vidore/
dinghy-law-family use, just without a highlighted row.
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.model_release import bars_card_data, cohort

BENCHMARK = "BRIGHT-Pro"
HERE = pathlib.Path(__file__).parent


def main() -> None:
    coh = cohort([], BENCHMARK, text_only=True)
    ranking = coh.all_comparable

    print(f"{BENCHMARK}: {len(ranking)} models with complete 7-task coverage\n")
    for i, e in enumerate(ranking, 1):
        print(f"  {i:>2}  {e.score:>6}  {(e.active_params or 0)/1e9:>5.2f}B active  {e.model}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_tasks": ranking[0].n_benchmark_tasks if ranking else 0,
        "n_models": len(ranking),
        "ranking": [e.as_dict() for e in ranking],
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # Top 10, not all 19: the bars template's row spacing is tuned for ~10 rows on the
    # 1200px canvas (see card-1-bright-pro.html's own comment), and the top 10 already
    # carries the story — the AQ-MedAI sweep of ranks 1-4 and where the familiar
    # general-purpose models (Qwen3-Embedding, gte-Qwen2) land relative to it. data.json
    # keeps the full 19, per CONTRIBUTING's "record every model that qualified."
    write_card_data(HERE / "card-1-bright-pro.html", bars_card_data(coh, top_n=10))
    print(f"\nwrote data.json ({len(ranking)} rows) and card data (top 10)")


if __name__ == "__main__":
    main()
