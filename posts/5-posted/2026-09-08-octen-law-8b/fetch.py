#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the litillabs/octen-law-8b-v1 post. Run from the repo root:

    uv run posts/3-review/octen-law-8b/fetch.py

mteb#5305 (merged 2026-08-26) registers `litillabs/octen-law-8b-v1`, a legal-retrieval
model adapted from `Octen/Octen-Embedding-8B`; results#688, same author, submits its
eight `MTEB(Law, v1)` results the next day. It takes 1st of the board.

**The check that decides whether this is postable at all.** The model's own `ModelMeta`
declares `GerDaLIRSmall` and `LeCaRDv2` as training data — two of the eight tasks it is
ranked on. A rank over a board that includes a model's own training set is not a
capability claim, so this script recomputes the ranking with every such task dropped. The
lead has to survive that, and the post has to say so either way.

Declared training data cannot be read from the leaderboard API, which reports only
whether training data is open at all. It is transcribed here from each model's
`ModelMeta` in `mteb/models/model_implementations/` at the merged revision, with the file
named per model, and every task name is checked against the live benchmark so a rename
or a typo fails the run instead of quietly excusing a model.

The asymmetry that transcription exposes is itself worth recording: of the top ten, only
two models declare any training data at all. "Declares nothing" is not "trained on
nothing", so the clean view below is a *lower* bound on overlap, not a clean room. The
post says that.
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.leaderboard_api import benchmark_scores, benchmark_task_scores
from mtebpost.model_release import bars_card_data, cohort

BENCHMARK = "MTEB(Law, v1)"
SUBJECT = "litillabs/octen-law-8b-v1"
HERE = pathlib.Path(__file__).parent

# model -> (source file in mteb/models/model_implementations/, declared training datasets)
# Transcribed from each ModelMeta; only entries that intersect this benchmark matter, but
# the empty ones are recorded too, because "declares nothing" is the finding.
DECLARED_TRAINING = {
    "litillabs/octen-law-8b-v1": ("litillabs_models.py", {"GerDaLIRSmall", "LeCaRDv2", "WikiQA"}),
    "Hanno-Labs/dinghy-law-8b-v1": ("hanno_labs_models.py", {"GerDaLIR", "GerDaLIRSmall", "BillSumUS"}),
    "Hanno-Labs/dinghy-law-4b-v1": ("hanno_labs_models.py", {"GerDaLIR", "GerDaLIRSmall", "BillSumUS"}),
    "Hanno-Labs/dinghy-law-0.6b-v1": ("hanno_labs_models.py", {"GerDaLIR", "GerDaLIRSmall", "BillSumUS"}),
    # Declared empty or None — the labs published no training-data list, not a list that
    # happens to exclude these tasks.
    "Mira190/Euler-Legal-Embedding-V1": ("euler_models.py", set()),
    "minetta/nemotron-3-embed-8b-legal": ("minetta_models.py", set()),
    "judicialmind/greenleaf-law-embed-tiny": ("greenleaf_models.py", set()),
    "voyageai/voyage-law-2": ("voyage_models.py", set()),
    "voyageai/voyage-3": ("voyage_models.py", set()),
    # F2LLM names seven of these eight tasks in codefuse_models.py — in its per-task
    # *instruction* dictionary, not in training_datasets, whose 57 entries include no
    # legal dataset. Checked, because a grep for the task name would say otherwise.
    "codefuse-ai/F2LLM-v2-14B": ("codefuse_models.py", set()),
}


def main() -> None:
    coh = cohort([SUBJECT], BENCHMARK)
    ranking = coh.all_comparable
    subject = coh.subjects[0]
    rank = ranking.index(subject) + 1
    runner_up = ranking[1]

    tasks, per_task = benchmark_task_scores(BENCHMARK)
    print(f"{BENCHMARK}: {len(tasks)} tasks, {len(ranking)} models with complete coverage")
    for i, e in enumerate(ranking[:10], 1):
        mark = "  <<< subject" if e.model == SUBJECT else ""
        print(f"  {i:>2}  {e.score:>6}  {(e.total_params or 0)/1e9:>5.2f}B  {e.model}{mark}")

    # Declared training tasks that are actually on this board.
    overlap = {}
    for model, (src, declared) in DECLARED_TRAINING.items():
        hit = sorted(declared & set(tasks))
        if hit:
            overlap[model] = hit
        print(f"\n{model}\n    declared in {src}: {sorted(declared) or 'nothing'}"
              f"\n    on this board: {hit or 'none'}")

    contaminated = sorted({t for hits in overlap.values() for t in hits})
    clean = [t for t in tasks if t not in contaminated]
    print(f"\ntasks declared as training data by at least one ranked model: {contaminated}")
    print(f"subject's own scores there: "
          f"{ {t: per_task[SUBJECT][t] for t in DECLARED_TRAINING[SUBJECT][1] & set(tasks)} }")

    # The ranking again, over the tasks nobody in the comparison declares.
    complete = [m for m, s in per_task.items() if len(s) == len(tasks)]
    clean_rank = sorted(
        ((round(sum(per_task[m][t] for t in clean) / len(clean), 2), m) for m in complete),
        reverse=True,
    )
    print(f"\nsame board over the {len(clean)} undeclared tasks:")
    for i, (s, m) in enumerate(clean_rank[:5], 1):
        print(f"  {i:>2}  {s:>6}  {m}")

    subj_clean = next(s for s, m in clean_rank if m == SUBJECT)
    second_clean = clean_rank[1]

    # Both claims, asserted rather than eyeballed: 1st on the board as published, and
    # still 1st once every declared-training task is removed.
    assert rank == 1, rank
    assert clean_rank[0][1] == SUBJECT, clean_rank[0]

    # Who is missing. A domain board is a fact about who submitted, so re-measure the
    # figure the dinghy-law post used rather than reusing a three-week-old number.
    eng_entries, _ = benchmark_scores("MTEB(eng, v2)")
    eng_top20 = [e.model for e in eng_entries if e.complete][:20]
    law_complete = {e.model for e in ranking}
    absent = [m for m in eng_top20 if m not in law_complete]
    print(f"\nof the top 20 on MTEB(eng, v2), {len(absent)} have no complete "
          f"{BENCHMARK} results: {absent}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_tasks": len(tasks),
        "n_models": len(ranking),
        "subject": SUBJECT,
        "subject_rank": rank,
        "subject_score": subject.score,
        "runner_up": {"model": runner_up.model, "score": runner_up.score},
        "margin": round(subject.score - runner_up.score, 2),
        "declared_training_data": {
            m: {"source": src, "declared": sorted(d), "on_this_board": sorted(d & set(tasks))}
            for m, (src, d) in DECLARED_TRAINING.items()
        },
        "undeclared_task_view": {
            "dropped": contaminated,
            "kept": clean,
            "subject_score": subj_clean,
            "runner_up": {"model": second_clean[1], "score": second_clean[0]},
            "margin": round(subj_clean - second_clean[0], 2),
            "subject_still_first": clean_rank[0][1] == SUBJECT,
            "ranking": [{"model": m, "score": s} for s, m in clean_rank],
        },
        "who_is_missing": {
            "question": "how many of the top 20 on MTEB(eng, v2) have complete Law results",
            "absent": absent,
            "n_absent": len(absent),
        },
        "per_task": {t: per_task[SUBJECT][t] for t in tasks},
        "ranking": [e.as_dict() for e in ranking],
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # Total parameters, not active: the previous post from this board
    # (2026-08-07-dinghy-law-family) sized its rows the same way, and a reader comparing
    # the two cards should not have to notice that the axis changed underneath them.
    data = bars_card_data(coh, top_n=10, size_field="total")
    for row in data["rows"]:
        if row.get("subject"):
            row["tag"] = f"this release · declares {len(overlap[SUBJECT])} of the {len(tasks)} tasks as training data"
    write_card_data(HERE / "card-1-octen-law-8b.html", data)
    print(f"\nwrote data.json ({len(ranking)} rows) and card data (top 10)")


if __name__ == "__main__":
    main()
