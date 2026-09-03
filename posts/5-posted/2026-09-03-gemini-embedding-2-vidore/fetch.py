#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the google/gemini-embedding-2 post. Run from the repo root:

    uv run posts/3-review/gemini-embedding-2-vidore/fetch.py

mteb#5220 registers `google/gemini-embedding-2` (GA), marks the preview superseded, and
implements interleaved text/image/audio/video input for it. results#679, same author,
submits its first results: `ViDoRe(v2)`, a registered 4-task benchmark, complete.

`ViDoRe(v2)` — not the 14-task `ViDoRe(v1&v2)`, on which this model has 4 of 14 and no
comparable aggregate at all. The scope is what was run, per CONTRIBUTING.md.

The story is not the rank on its own. Every model above it on this board is a
late-interaction (multi-vector) retriever — a different architecture, one that stores a
vector per patch instead of one per document — and `gemini-embedding-2` is the
highest-scoring single-vector model on the board. That is the fact worth a post: an
architecture comparison the benchmark's own leaderboard makes visible, on a board where
the two families are otherwise easy to conflate.

`model_types()` reads each model's architecture from its registry `ModelMeta`, so the
split is not inferred from names — "Col*" is a naming convention, not a fact.

Two cards, because the claim has two halves and neither picture carries both:

- `card-1-single-vector`: the 13 single-vector models, the cohort the subject leads.
- `card-2-board`: the whole board, with ranks 11-20 drawn as an explicit stand-in row
  rather than silently skipped — the numbers in that row are computed here.
"""

import json
import pathlib
from datetime import date

from mtebpost.cards import write_card_data
from mtebpost.leaderboard_api import model_types
from mtebpost.model_release import bars_card_data, cohort, recommend_chart

BENCHMARK = "ViDoRe(v2)"
SUBJECT = "google/gemini-embedding-2"
HERE = pathlib.Path(__file__).parent

# How the card labels each row. The registry's own vocabulary ("dense",
# "late-interaction") is accurate but not self-explanatory on an image; these say the
# same thing in the words the claim uses.
ARCH_LABEL = {"dense": "single-vector", "late-interaction": "late-interaction"}


def main() -> None:
    # text_only=False: this is a document-image benchmark and several entrants declare
    # image modalities only. The text filter exists to keep English-only models off a
    # multilingual text board (CONTRIBUTING's cohort-fairness rule); here it would drop
    # models that are exactly the intended competition.
    coh = cohort([SUBJECT], BENCHMARK, text_only=False)
    ranking = coh.all_comparable
    subject = coh.subjects[0]
    rank = ranking.index(subject) + 1

    rec = recommend_chart(coh)
    print(f"recommend_chart: {rec.chart} — {rec.reason}\n")

    types = model_types()
    arch = {e.model: types.get(e.model, "unknown") for e in ranking}

    print(f"{BENCHMARK}: {len(ranking)} models with complete {coh.n_benchmark_tasks}-task coverage")
    for i, e in enumerate(ranking, 1):
        mark = "  <<< subject" if e.model == SUBJECT else ""
        print(f"  {i:>2}  {e.score:>6}  {arch[e.model]:<18} {e.model}{mark}")

    above = ranking[: rank - 1]
    arch_above = sorted({arch[e.model] for e in above})
    same_arch = [e for e in ranking if arch[e.model] == arch[SUBJECT]]
    best_same_arch = same_arch[0].model if same_arch else None
    runner_up = same_arch[1] if len(same_arch) > 1 else None

    print(f"\nsubject rank: {rank} of {len(ranking)}  ({subject.score})")
    print(f"architectures above it: {arch_above}")
    print(f"best {arch[SUBJECT]} model: {best_same_arch}")
    if runner_up:
        print(f"next {arch[SUBJECT]} model: {runner_up.model} at {runner_up.score}")

    # The two claims the post makes, checked here rather than read off the printout.
    assert arch_above == ["late-interaction"], arch_above
    assert best_same_arch == SUBJECT, best_same_arch

    counts: dict[str, int] = {}
    for e in ranking:
        counts[arch[e.model]] = counts.get(arch[e.model], 0) + 1
    print(f"cohort by architecture: {counts}")

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_tasks": coh.n_benchmark_tasks,
        "n_models": len(ranking),
        "subject": SUBJECT,
        "subject_rank": rank,
        "subject_score": subject.score,
        "architectures_above_subject": arch_above,
        "best_of_subject_architecture": best_same_arch,
        "runner_up_same_architecture": (
            {"model": runner_up.model, "score": runner_up.score} if runner_up else None
        ),
        "cohort_by_architecture": counts,
        "per_task": {t: s for t, s in sorted(coh.per_task[SUBJECT].items())},
        "ranking": [{**e.as_dict(), "model_type": arch[e.model]} for e in ranking],
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    # --- card 1: one architecture, all of it -------------------------------------
    # Every single-vector model with complete coverage, ranked among themselves. This is
    # a cohort of one architecture, so the rank on this card is a rank within it — not
    # the board rank, which is card 2's subject.
    same = [e for e in ranking if arch[e.model] == arch[SUBJECT]]
    n_other_arch = len(ranking) - len(same)
    write_card_data(HERE / "card-1-single-vector.html", {
        "benchmark": BENCHMARK,
        "n_tasks": coh.n_benchmark_tasks,
        "n_models": len(same),
        "n_late_interaction": n_other_arch,
        "rows": [
            {
                "model": e.model, "score": e.score, "params": e.total_params,
                "rank": i, **({"subject": True} if e.model == SUBJECT else {}),
            }
            for i, e in enumerate(same, 1)
        ],
    })

    # --- card 2: the whole board, with the skipped ranks stated -------------------
    # Top 10 plus the subject at 21. bars_card_data keeps the true board rank on every
    # row, so the subject's row reads 21 rather than 11.
    data = bars_card_data(coh, top_n=10, size_field="total")
    for row in data["rows"]:
        row["arch"] = ARCH_LABEL.get(arch[row["model"]], arch[row["model"]])

    # The rows between the last drawn one and the subject are not omitted, they are
    # summarised: how many, what they are, and the range they cover. Computed, so the
    # card cannot drift from the board it describes.
    first_shown_gap, last_shown_gap = 11, rank - 1
    skipped = ranking[first_shown_gap - 1 : last_shown_gap]
    if skipped:
        archs = sorted({arch[e.model] for e in skipped})
        note = (
            f"all {ARCH_LABEL.get(archs[0], archs[0])}" if len(archs) == 1
            else ", ".join(ARCH_LABEL.get(a, a) for a in archs)
        )
        gap_row = {
            "gap": True, "from": first_shown_gap, "to": last_shown_gap,
            "n": len(skipped), "note": note,
            "high": skipped[0].score, "low": skipped[-1].score,
        }
        subject_idx = next(i for i, r in enumerate(data["rows"]) if r.get("subject"))
        data["rows"].insert(subject_idx, gap_row)
        print(f"gap row: ranks {first_shown_gap}-{last_shown_gap}, {note}, "
              f"{skipped[0].score} down to {skipped[-1].score}")

    write_card_data(HERE / "card-2-board.html", data)
    print(f"\nwrote data.json ({len(ranking)} rows), card 1 ({len(same)} single-vector "
          f"models) and card 2 (top 10, a gap row, and the subject)")


if __name__ == "__main__":
    main()
