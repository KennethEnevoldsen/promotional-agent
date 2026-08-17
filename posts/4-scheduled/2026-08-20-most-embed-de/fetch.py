#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the most-embed-de post. Run from the repo root:

    uv run posts/2-drafting/most-embed-de/fetch.py

This is the first real use of `mtebpost.model_release` — the template extracted from
bekko-thread/dinghy-law-family/colvec11-vidore/mdenseon-mlateon once those four repeated
the same cohort-selection and chart-shape work by hand each time (docs/card-design.md).
It runs entirely on the live leaderboard-backend API (`mtebpost.leaderboard_api`), not
the local `mteb` library: the local package is version-pinned for reproducibility
(pyproject.toml's `exclude-newer`, dated 2026-07-30) and so has no `ModelMeta` for
`malteos/most-embed-de` (registered 2026-08-11) at all — the same reason
colvec11-vidore/dinghy-law-family/mdenseon-mlateon already use this API rather than
`mtebpost.scoreboard`. No `mtebpost[leaderboard]` extra needed here either: no `mteb`
import, no torch/transformers, a plain HTTP call.

`malteos/most-embed-de` was evaluated on 6 tasks — GerDaLIR, GerDaLIRSmall, GermanDPR,
GermanQuAD-Retrieval, MIRACLReranking, XMarket — not a registered MTEB benchmark. That is
a German-retrieval slice, not full MTEB(deu, v1) (19 tasks, including
classification/clustering/STS this model was never run on). The "full task coverage"
rule still applies; it is just scoped to what was actually run. XMarket and
MIRACLReranking are themselves multi-language tasks (subsets include "en"/"es"/"ar"/etc.
alongside "de") — the API reports no aggregate score for a model that ran fewer than
every subset a task has, so SUBSETS below pins both to "de", the only one this model (or
any single-language German model) could ever complete. That is the same scoping the
registered MTEB(deu, v1) benchmark itself uses for these two tasks.

`nvidia/Nemotron-3-Embed-1B-BF16` is checked directly because mteb#5149's own PR body
names it as the intended comparison ("mirrors the base model's entry exactly, so results
are directly comparable") and `adapted_from` records the same fact in the ModelMeta —
recommend_chart()'s peer-pool heuristic has no way to know that a specific model is *the*
comparison rather than just the closest score, so it is checked directly rather than
left to the automatic pick.
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.model_release import (
    bars_card_data,
    cohort,
    pareto_card_data,
    radar_card_data,
    recommend_chart,
)

SUBJECT = "malteos/most-embed-de"
BASE_MODEL = "nvidia/Nemotron-3-Embed-1B-BF16"  # adapted_from — the named comparison
TASKS = [
    "GerDaLIR", "GerDaLIRSmall", "GermanDPR",
    "GermanQuAD-Retrieval", "MIRACLReranking", "XMarket",
]
SUBSETS = {"XMarket": "de", "MIRACLReranking": "de"}
HERE = pathlib.Path(__file__).parent


def main() -> None:
    coh = cohort(
        [SUBJECT], TASKS, name="German Retrieval (6 tasks, custom subset)",
        subsets=SUBSETS, text_only=True,
    )
    subject = coh.subjects[0]

    print(f"{SUBJECT}: {subject.score} on {len(TASKS)} German-retrieval tasks "
          f"({(subject.active_params or 0)/1e6:.0f}M active, "
          f"{(subject.total_params or 0)/1e6:.0f}M total)")
    print(f"peers with full coverage of the same {len(TASKS)} tasks: {len(coh.peers)}")
    for p in coh.peers:
        print(f"  {p.score:>6}  {(p.active_params or 0)/1e6:>7.0f}M active  {p.model}")
    if coh.excluded:
        print(f"excluded (partial coverage or unknown size): {len(coh.excluded)}")
        for e in coh.excluded:
            print(f"  {e.model}: {e.n_tasks}/{e.n_benchmark_tasks} tasks")

    base = next((e for e in coh.pool if e.model == BASE_MODEL), None)
    if base:
        print(f"\nbase model {BASE_MODEL}: {base.score} on {base.n_tasks}/{len(TASKS)} tasks "
              f"({'+' if subject.score >= base.score else ''}{subject.score - base.score:.2f} vs subject)")
    else:
        print(f"\n{BASE_MODEL}: no results at all on this 6-task subset")

    rec = recommend_chart(coh)
    print(f"\nrecommend_chart: {rec.chart} — {rec.reason}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": coh.benchmark,
        "tasks": TASKS,
        "subsets": SUBSETS,
        "cohort_rule": f"full coverage of the same {len(TASKS)} German-retrieval tasks",
        "subject": subject.as_dict(),
        "base_model": base.as_dict() if base else None,
        "peers": [p.as_dict() for p in coh.peers],
        "excluded": [e.as_dict() for e in coh.excluded],
        "chart_recommendation": {"chart": rec.chart, "reason": rec.reason},
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # The base-model comparison is checked directly above rather than trusted to
    # recommend_chart() alone (see the module docstring) — draft against whichever
    # shape actually fits once these numbers are in, then delete the branches not used.
    if rec.chart == "pareto":
        write_card_data(HERE / "card-1-most-embed-de.html", pareto_card_data(coh))
    elif rec.chart == "radar" or (base and base.plottable):
        roles = {SUBJECT: "subject"}
        if base and base.plottable:
            roles[BASE_MODEL] = "highlight"
        for p in coh.peers[:3]:
            if p.model not in roles:
                roles[p.model] = "reference"
        write_card_data(HERE / "card-1-most-embed-de.html", radar_card_data(coh, roles))
    else:
        write_card_data(
            HERE / "card-1-most-embed-de.html",
            bars_card_data(coh, prior=(BASE_MODEL,) if base else ()),
        )

    print(f"\nwrote data.json ({len(coh.peers) + 1} scored models) and a {rec.chart} card")


if __name__ == "__main__":
    main()
