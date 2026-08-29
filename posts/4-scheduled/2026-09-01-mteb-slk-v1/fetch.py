#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the MTEB(slk, v1) benchmark_addition post. Run from the repo root:

    uv run posts/3-review/mteb-slk-v1/fetch.py

mteb#4788 registers `MTEB(slk, v1)` (SkMTEB, arXiv:2606.13647) — 31 Slovak tasks across
7 task types, 17 of them defined by that same PR. results#570, same author, submits
day-one results for ~20 models, which is why this is a benchmark post with a board
rather than a bare announcement.

No single model is the subject: `cohort([], BENCHMARK)` with an empty subject list, the
same builder BRIGHT-Pro used.

Two things this script checks rather than assumes:

- **Task types.** The "7 task types" figure is read from each task's own metadata
  (`leaderboard_api.task_type()`), not from the section comments in the PR's benchmark
  definition, which are a contributor's hand-typed labels.
- **Who the missing model changes.** Only 8 of the ~20 models in results#570 have all
  31 tasks; 11 more are short by exactly one task, `WebFAQRetrieval`. A ranking over
  the models that happen to be complete is a fact about submission timing, so the
  30-task view is recomputed here as well. If the two disagree at the top, the post
  cannot lead with a rank (CONTRIBUTING.md, "ask who is missing before believing a
  ranking").
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.leaderboard_api import benchmark_task_scores, task_type
from mtebpost.model_release import cohort

BENCHMARK = "MTEB(slk, v1)"
HERE = pathlib.Path(__file__).parent

# The 17 task classes mteb#4788 defines itself, read off the merged diff
# (`^\+class X(AbsTask...)`) and confirmed imported into each package's `__init__.py` —
# a class that is defined but never imported is not reachable through `mteb.get_task()`.
# The other 14 tasks in the benchmark already existed, either as Slovak tasks
# (SKQuadRetrieval, SlovakSumRetrieval, SlovakHateSpeechClassification.v2,
# SlovakMovieReviewSentimentClassification.v2) or as multilingual ones pinned to their
# Slovak subsets (Tatoeba, FloresBitextMining, NTREXBitextMining, the two WebFAQ bitext
# tasks, WebFAQRetrieval, BelebeleRetrieval, SIB200Classification, SIB200ClusteringS2S,
# MultilingualSentimentClassification).
NEW_IN_PR = [
    "OpusSlovakEnglishBitextMining",
    "MultiEupSlovakPartyClassification",
    "MultiEupSlovakGenderClassification",
    "SlovakParlaSentClassification",
    "PravdaSKTagClustering",
    "PravdaSKURLClustering",
    "SlovakSumURLClustering",
    "SMESumCategoryClustering",
    "DemagogSKNLI",
    "SlovakNLI",
    "SlovakRTE",
    "SkQuadReranking",
    "SlovakPharmacyDrMaxReranking",
    "SlovakPharmacyMojaLekarenReranking",
    "SMESumRetrieval",
    "SlovakSTS",
    "SlovakSumSTS",
]


def main() -> None:
    coh = cohort([], BENCHMARK, text_only=True)
    ranking = coh.all_comparable

    # Same endpoint the cohort came from, but keeping the partial-coverage rows: the
    # task-type census and the 30-task check below are both questions about models the
    # board itself leaves out.
    tasks, per_task = benchmark_task_scores(BENCHMARK)
    types = {t: task_type(t) for t in tasks}
    by_type: dict[str, list[str]] = {}
    for t, tt in types.items():
        by_type.setdefault(tt, []).append(t)

    print(f"{BENCHMARK}: {len(tasks)} tasks, {len(by_type)} task types")
    for tt, ts in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        new = sum(1 for t in ts if t in NEW_IN_PR)
        print(f"  {tt:20s} {len(ts):>2} tasks ({new} new in mteb#4788)")

    print(f"\n{len(ranking)} models with complete {len(tasks)}-task coverage:")
    for i, e in enumerate(ranking, 1):
        print(f"  {i:>2}  {e.score:>6}  {(e.total_params or 0)/1e6:>6.0f}M total  {e.model}")

    # The robustness check. `WebFAQRetrieval` is the one task 11 otherwise-complete
    # models are missing; dropping it more than doubles the board. If the leader is the
    # same either way, the rank is a fact about the models rather than about who
    # finished submitting first — and only then may the post state it.
    DROP = "WebFAQRetrieval"
    kept = [t for t in tasks if t != DROP]
    without = []
    for model, scores in per_task.items():
        if all(t in scores for t in kept):
            without.append((round(sum(scores[t] for t in kept) / len(kept), 2), model))
    without.sort(reverse=True)
    print(f"\nsame board with {DROP} dropped — {len(without)} models:")
    for i, (s, m) in enumerate(without, 1):
        print(f"  {i:>2}  {s:>6}  {m}")
    agree = bool(ranking) and bool(without) and ranking[0].model == without[0][1]
    print(f"\nleader agrees across both views: {agree}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "task_types": {tt: sorted(ts) for tt, ts in sorted(by_type.items())},
        "new_in_mteb_4788": NEW_IN_PR,
        "n_models_complete": len(ranking),
        "ranking": [e.as_dict() for e in ranking],
        "robustness_check": {
            "dropped_task": DROP,
            "why": f"11 models have every task except {DROP}",
            "n_models": len(without),
            "ranking": [{"model": m, "score": s} for s, m in without],
            "leader_unchanged": agree,
        },
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # One highlighted task per task type, chosen for what a reader could not guess from
    # "31 tasks across 7 task types" — the card carries a sentence about each. Editorial
    # picks, so they live here rather than being derived, but the names and types are
    # checked against the live benchmark: a highlight that does not exist, or whose type
    # was assumed rather than read, fails the run instead of reaching the card.
    HIGHLIGHTS = [
        "SlovakPharmacyDrMaxReranking",
        "DemagogSKNLI",
        "SlovakParlaSentClassification",
        "PravdaSKTagClustering",
        "SMESumRetrieval",
        "SlovakSTS",
    ]
    unknown = [t for t in HIGHLIGHTS if t not in tasks]
    if unknown:
        raise SystemExit(f"highlighted tasks not in {BENCHMARK}: {unknown}")
    not_new = [t for t in HIGHLIGHTS if t not in NEW_IN_PR]
    if not_new:
        raise SystemExit(f"highlighted tasks are not new in mteb#4788: {not_new}")

    write_card_data(
        HERE / "card-1-mteb-slk-v1.html",
        {
            "n_tasks": len(tasks),
            "n_new": len(NEW_IN_PR),
            "n_types": len(by_type),
            "n_models_complete": len(ranking),
            "by_type": [
                {
                    "type": tt,
                    "new": sum(1 for t in ts if t in NEW_IN_PR),
                    "existing": sum(1 for t in ts if t not in NEW_IN_PR),
                }
                for tt, ts in sorted(by_type.items(), key=lambda kv: -len(kv[1]))
            ],
            "highlights": [{"task": t, "type": types[t]} for t in HIGHLIGHTS],
        },
    )
    print(f"\nwrote data.json ({len(ranking)} ranked models) and card data")


if __name__ == "__main__":
    main()
