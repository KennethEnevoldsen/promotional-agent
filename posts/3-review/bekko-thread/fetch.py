#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost[leaderboard]"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
#
# [tool.uv]
# exclude-newer = "2026-08-01T00:00:00Z"
# ///
"""Evidence for the Bekko post. Run from the repo root:

    uv run posts/2026-08-03-bekko-frontier/fetch.py

Writes data.json (the full cohort) and the numbers into card.html's #card-data.

The frontier post: this card needs the cohort but not the large reference, which
would stretch a log axis out to 7B and squash the cohort into the left margin.

The claim the post wants to make is "very small model, competitive score", which is
only meaningful against models of a comparable size. So the cohort is every text model
in the results repo with an active-parameter count at or below 60M — a band wide enough
to include real competition for a 7.7M and a 24.9M model without stretching to compare
against 7B models that would make any small model look bad.

Peers must also declare more than one language. This is not a detail. Without it the
cohort picks up e5-small-v2, bge-small-en-v1.5 and all-MiniLM-L6-v2 — English-only
models sitting at the bottom of a 131-task multilingual benchmark. They score low
because they were never built for this, so including them would both inflate Bekko's
apparent margin and imply three well-regarded models are worse than they are.

Static embedding models belong in this cohort. Their active count is 0 — a real value,
not a missing one, since every parameter sits in the lookup table and nothing is
computed per token. They are the limiting case of exactly the design Bekko is pitching,
which makes them the most informative peers available: the gap between them and Bekko is
what 7.7M active parameters actually buys.

Cohort membership is a judgement call and it is the one thing in the post a reader
cannot check. Hence this file: the band, the language floor, the benchmark and the date
are recorded here, and data.json holds every model that qualified at each stage — not
just the flattering ones.
"""

import json
import pathlib
from datetime import date


from mtebpost.cards import write_card_data
from mtebpost.scoreboard import rank_of, scores, size_peers

BENCHMARK = "MTEB(Multilingual, v2)"
MAX_ACTIVE = 60_000_000
MIN_LANGUAGES = 2  # multilingual benchmark: English-only models are not peers
SUBJECTS = [
    "hotchpotch/bekko-embedding-v1-a8m",
    "hotchpotch/bekko-embedding-v1-a25m",
]

# A large model carried purely as a scale reference: it sits ~280x above the size cap,
# so it is not a peer and must never be drawn as one. It answers the question the size
# cohort cannot — "and where is the field overall?" — which otherwise leaves a reader
# thinking 58 is a good absolute score when it is a good score *for 25M parameters*.
# Flagged `reference` so each card can decide: the bar card draws it dashed and outside
# the ranking, the scatter drops it rather than stretch its axis to 7B.
REFERENCE = "Qwen/Qwen3-Embedding-8B"

HERE = pathlib.Path(__file__).parent


# Models are identified by their full Hugging Face name everywhere — on the card, in the
# post text and in data.json. Abbreviations save space but make a claim harder to check
# against the leaderboard, and two models can abbreviate to the same thing.
# The card splits the name at "/" across two lines rather than shortening it.


def main() -> None:
    cohort = sorted(
        set(size_peers(max_active=MAX_ACTIVE, min_languages=MIN_LANGUAGES)) | set(SUBJECTS)
    )
    print(
        f"cohort candidates: {len(cohort)} models <= {MAX_ACTIVE/1e6:.0f}M active"
        f", >= {MIN_LANGUAGES} languages"
    )

    entries = scores(BENCHMARK, cohort + [REFERENCE])
    reference = next((e for e in entries if e.model == REFERENCE), None)
    entries = [e for e in entries if e.model != REFERENCE]
    print(f"with any results on {BENCHMARK}: {len(entries)} (+ reference {REFERENCE})")

    plottable = [e for e in entries if e.plottable]
    excluded = [e for e in entries if not e.plottable]
    print(f"comparable (full task coverage + known size): {len(plottable)}")
    for e in excluded:
        why = "partial task coverage" if not e.complete else "no active-parameter count"
        print(f"  excluded: {e.model} ({why}, {e.n_tasks}/{e.n_benchmark_tasks} tasks)")

    ranks = {}
    for s in SUBJECTS:
        r, n = rank_of(plottable, s)
        ranks[s] = {"rank": r, "of": n}
        print(f"  {s}: rank {r} of {n} comparable")

    data = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "cohort_rule": (
            f"multilingual text models (>= {MIN_LANGUAGES} languages) "
            f"with <= {MAX_ACTIVE/1e6:.0f}M active parameters"
        ),
        "comparability_rule": "full task coverage on the benchmark and a known active-parameter count",
        "subjects": SUBJECTS,
        "ranks": ranks,
        "entries": [e.as_dict() for e in entries],
    }
    (HERE / "data.json").write_text(json.dumps(data, indent=2) + "\n")

    # Data only — no prose. Values, not phrasings: `max_active_params` rather than a
    # sentence about the cohort, so the card decides how to word it. Every human-written
    # sentence lives in the COPY object at the top of card.html.
    #
    # Written straight into card.html's #card-data block, so the file you open in a
    # browser is the file that renders. There is no intermediate card.json to drift.
    card = {
        "benchmark": BENCHMARK,
        "n_tasks": plottable[0].n_benchmark_tasks,
        "max_active_params": MAX_ACTIVE,
        "n_models": len(plottable),
        "points": [
            {
                "model": e.model,
                "x": e.active_params,
                "total": e.total_params,
                "y": e.score,
                **({"subject": True} if e.model in SUBJECTS else {}),
            }
            for e in plottable
        ] + ([{
            "model": reference.model,
            "x": reference.active_params,
            "total": reference.total_params,
            "y": reference.score,
            "reference": True,
        }] if reference and reference.plottable else []),
    }
    write_card_data(HERE / "card-1-frontier.html", card)
    print(f"wrote data.json ({len(entries)} rows) and card data ({len(plottable)} points)")

    print("\ncomparable cohort:")
    for e in plottable:
        mark = "*" if e.model in SUBJECTS else " "
        active = e.active_params or 0  # plottable guarantees not None; 0 means static
        size = "static" if e.is_static else f"{active/1e6:.1f}M"
        print(f" {mark} {e.score:>6}  {size:>8}  {e.model}")


if __name__ == "__main__":
    main()
