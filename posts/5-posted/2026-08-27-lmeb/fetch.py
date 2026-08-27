#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the LMEB post. Run from the repo root:

    uv run posts/2-drafting/lmeb/fetch.py

Trigger is results#670, "Add LMEB Evaluation Results of 12 Embedding Models" — 12
different models (4 opensearch-project neural-sparse encoders, LiquidAI/
LFM2.5-Embedding-350M, perplexity-ai/pplx-embed-v1-0.6b, 6 ibm-granite variants), none
registered in this scan window, so this is a `results_addition` per CONTRIBUTING.md, not
a model_addition. LMEB (Long-horizon Memory Embedding Benchmark, mteb#4614) itself is not
new either — registered back in May and already has 70 models with complete coverage.

The story isn't "12 models landed at once" (a batch with no shared claim is not one post
— CONTRIBUTING's "one post, one claim"). It's that two of the twelve —
`opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini` (11M active) and
`-doc-v2-distill` (43M active) — sit on LMEB's actual Pareto frontier across the full
70-model board, not just among the 12 new arrivals: nothing smaller scores higher, at
any size up to Nemotron-3-Embed-8B-BF16 (7.4B active). That is a real, checkable
efficiency claim in the family this account already covers (bekko, most-embed-de), on a
benchmark it has never covered before (breadth).
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.model_release import cohort, pareto_card_data, recommend_chart

BENCHMARK = "LMEB"
SUBJECTS = [
    "opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini",
]
# The rest of the 12-model batch (results#670) — not subjects of the claim, but named
# for credit in the post text and checked here so their placement is on record.
# v2-distill is here rather than in SUBJECTS despite also being on the frontier: its
# name is close enough in length and position to v2-mini's that both as labeled card
# subjects collide (tried it — even a forced LABEL_SIDE split ran the wider label off
# the canvas edge). One clean subject beats two crowded ones; v2-distill is still named
# in the post text and data.json.
OTHER_NEW_MODELS = [
    "opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill",
    "opensearch-project/opensearch-neural-sparse-encoding-doc-v3-gte",
    "opensearch-project/opensearch-neural-sparse-encoding-doc-v3-distill",
    "LiquidAI/LFM2.5-Embedding-350M",
    "perplexity-ai/pplx-embed-v1-0.6b",
    "ibm-granite/granite-embedding-small-english-r2",
    "ibm-granite/granite-embedding-english-r2",
    "ibm-granite/granite-embedding-30m-english",
    "ibm-granite/granite-embedding-278m-multilingual",
    "ibm-granite/granite-embedding-125m-english",
    "ibm-granite/granite-embedding-107m-multilingual",
]
HERE = pathlib.Path(__file__).parent


def main() -> None:
    coh = cohort(SUBJECTS, BENCHMARK, text_only=True)

    print(f"{BENCHMARK}: {len(coh.peers) + len(SUBJECTS)} models with complete "
          f"{coh.n_benchmark_tasks}-task coverage\n")
    for s in coh.subjects:
        print(f"  subject  {s.score:>6}  {(s.active_params or 0)/1e6:>7.0f}M active  {s.model}")

    rec = recommend_chart(coh)
    print(f"\nrecommend_chart: {rec.chart} — {rec.reason}")
    for m, why in rec.per_subject.items():
        print(f"  {m}: {why}")

    by_name = {e.model: e for e in coh.pool}
    others = [by_name[m] for m in OTHER_NEW_MODELS if m in by_name]
    ranking = coh.all_comparable
    rank_of = {e.model: i for i, e in enumerate(ranking, 1)}
    print(f"\nrest of results#670's 12-model batch ({len(others)}/{len(OTHER_NEW_MODELS)} found):")
    for e in sorted(others, key=lambda e: -e.score):
        print(f"  {rank_of.get(e.model, '?'):>3} of {len(ranking)}  {e.score:>6}  {e.model}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": coh.benchmark,
        "n_tasks": coh.n_benchmark_tasks,
        "n_models": len(ranking),
        "subjects": [s.as_dict() for s in coh.subjects],
        "other_new_models": [
            {"model": e.model, "rank": rank_of.get(e.model), "score": e.score}
            for e in others
        ],
        "chart_recommendation": {"chart": rec.chart, "reason": rec.reason},
        "ranking": [e.as_dict() for e in ranking],
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    write_card_data(HERE / "card-1-lmeb.html", pareto_card_data(coh))
    print(f"\nwrote data.json ({len(ranking)} models) and a {rec.chart} card")


if __name__ == "__main__":
    main()
