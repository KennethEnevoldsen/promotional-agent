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
"""Evidence for the efficiency-frontier post. Run from the repo root:

    uv run posts/2026-08-17-efficiency-frontier/fetch.py

Slow — roughly 15 minutes, because the claim is about the whole field over time and a
sampled field is not a field.

The question: how much compute does a given quality of embedding cost, and how has that
changed? For each cutoff date, take every model released on or before it and compute the
Pareto frontier of score against *active* parameters — the models nothing smaller beats.
Three frontiers, three years apart, on one axis.

Active parameters, not total: for models with a large shared embedding table the two
differ by more than 10x, and active is what a GPU actually runs.

Static embedding models are included, at exactly 0 active parameters. This is not an
edge case to filter out — `minishlab/potion-base-32M` scores 54.63 with no active
parameters at all, which puts it *on* the current frontier and above two models that
would otherwise appear on it. Dropping zero-active models (the easy mistake: `if
active:` treats 0 as missing) would quietly redraw the frontier's whole left end.

Caveats the post has to carry:

* Only 20 models with complete results were released by end-2023, so the earliest
  frontier is sparse and sits lower than the true 2023 state of the art would have.
* These are release dates, not evaluation dates. A model released in 2023 may have been
  submitted to MTEB much later, so each frontier reflects what *exists* by that date and
  is known now — not what the leaderboard showed then.
"""

import json
import pathlib
import warnings
from datetime import date

warnings.filterwarnings("ignore")


import mteb

from mtebpost.cards import write_card_data

BENCHMARK = "MTEB(eng, v2)"
CUTOFFS = [("2023", "2023-12-31"), ("2024", "2024-12-31"), ("today", "2099-12-31")]
HERE = pathlib.Path(__file__).parent


def frontier(rows: list[dict]) -> list[dict]:
    """Models nothing smaller-or-equal beats: sort by size, keep each new best score."""
    out: list[dict] = []
    for r in sorted(rows, key=lambda r: (r["x"], -r["y"])):
        if not out or r["y"] > out[-1]["y"]:
            out.append(r)
    return out


def main() -> None:
    bench = mteb.get_benchmark(BENCHMARK)
    n_bench = len(bench.tasks)
    metas = {m.name: m for m in mteb.get_model_metas()}

    print(f"scoring {len(metas)} models on {BENCHMARK} ({n_bench} tasks) — ~15 min")
    results = mteb.load_results(tasks=bench.tasks, models=list(metas), only_main_score=True)
    agg = bench.get_score(results)

    covered: dict[str, int] = {}
    for mr in results.model_results:
        covered[mr.model_name] = max(covered.get(mr.model_name, 0), len(mr.task_results))

    rows = []
    for name, row in agg.items():
        s = row.get("Mean(Task)")
        meta = metas.get(name)
        if s is None or meta is None:
            continue
        if covered.get(name, 0) != n_bench:
            continue
        active = meta.n_active_parameters
        if active is None or not meta.release_date:
            continue  # 0 is a real value and stays; None is genuinely unknown
        rows.append({
            "model": name,
            "x": active,
            "y": round(s * 100, 2) if s <= 1 else round(s, 2),
            "released": str(meta.release_date),
        })

    cohorts = []
    for label, cut in CUTOFFS:
        eligible = [r for r in rows if r["released"] <= cut]
        cohorts.append({
            "label": label,
            "cutoff": cut,
            "n_models": len(eligible),
            "points": frontier(eligible),
        })

    # the headline: what the best score of 2023 costs today
    by_2023 = [r for r in rows if r["released"] <= "2023-12-31"]
    best23 = max(by_2023, key=lambda r: r["y"])
    matches = [r for r in rows if r["y"] >= best23["y"]]
    cheapest = min(matches, key=lambda r: r["x"])

    headline = {
        "best_2023": best23,
        "cheapest_match_today": cheapest,
        "shrink_factor": round(best23["x"] / cheapest["x"], 1) if cheapest["x"] else None,
    }

    (HERE / "data.json").write_text(json.dumps({
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_benchmark_tasks": n_bench,
        "rule": "complete task coverage, known active-parameter count, known release date",
        "note": "release dates, not evaluation dates; the 2023 cohort is sparse",
        "headline": headline,
        "cohorts": cohorts,
        "models": sorted(rows, key=lambda r: -r["y"]),
    }, indent=2) + "\n")

    write_card_data(HERE / "card.html", {
        "benchmark": BENCHMARK,
        "n_tasks": n_bench,
        "n_models": len(rows),
        "headline": headline,
        "cohorts": cohorts,
    })

    print(f"\n{len(rows)} models with complete results, known size and release date")
    for c in cohorts:
        print(f"  {c['label']:>6}: {c['n_models']:>3} models, {len(c['points'])} on the frontier")
    print(f"\nbest by end-2023: {best23['y']} at {best23['x']/1e6:.1f}M ({best23['model']})")
    print(f"matched today at: {cheapest['y']} at {cheapest['x']/1e6:.1f}M ({cheapest['model']})")
    print(f"shrink: {headline['shrink_factor']}x fewer active parameters")


if __name__ == "__main__":
    main()
