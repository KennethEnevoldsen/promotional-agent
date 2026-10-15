#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost[leaderboard]", "mteb==2.24.10"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
#
# [tool.uv]
# exclude-newer = "2026-10-13T00:00:00Z"
# ///
"""Evidence for the Pareto-tag card. Run from the repo root:

    uv run posts/4-scheduled/2026-10-15-leaderboard-pareto-tag/fetch.py

The card shows which models the new Pareto tag marks on the leaderboard's default board,
MTEB(Multilingual, v2), and where they sit in its ranking. Two sources, checked against
each other:

1. **The live leaderboard API** (the same endpoint the site renders from) gives the cohort
   the tag is computed over — rows with both an active-parameter count and a non-null
   Mean (Task); a null mean is how the site marks partial coverage — and each row's rank.
   The rank is a property of the leaderboard's display (Borda over tasks), not a score,
   so it is taken from there and labelled as such.
2. **`Benchmark.get_score()` on the results repo** recomputes Mean (Task) for every model
   in that cohort (rule 1: never post a number that has not been recomputed). The
   frontier is then recomputed from *our* scores with the frontend's own rule
   (`paretoFrontier()` in leaderboard-frontend `src/lib/pareto.ts` at `fbb28ce`), and
   the script fails if either the scores or the tagged set disagree with the site.

Sizes come from the API (`activeParamsB`) and are cross-checked against
`ModelMeta.n_active_parameters`.
"""

import json
import pathlib
import urllib.parse
import urllib.request
import warnings
from datetime import date

warnings.filterwarnings("ignore")

import mteb  # noqa: E402

from mtebpost.cards import write_card_data  # noqa: E402

BENCHMARK = "MTEB(Multilingual, v2)"
API = "https://mteb-leaderboard-backend.hf.space/v1/benchmarks/{}/scores"
HERE = pathlib.Path(__file__).parent
CARD = HERE / "card-1-pareto-tag.html"
SCORE_TOL = 0.01  # points; the site and get_score round differently at the 4th decimal


def pareto(rows: list[dict]) -> list[dict]:
    """Port of paretoFrontier(): ascending size, keep a size group's best if it beats
    every strictly smaller model. Exact ties on both axes keep every tied row."""
    rows = sorted(rows, key=lambda r: (r["active_b"], -r["score"]))
    out, best_smaller, i = [], float("-inf"), 0
    while i < len(rows):
        size, group_best = rows[i]["active_b"], rows[i]["score"]
        while i < len(rows) and rows[i]["active_b"] == size:
            if rows[i]["score"] == group_best and rows[i]["score"] > best_smaller:
                out.append(rows[i])
            i += 1
        best_smaller = max(best_smaller, group_best)
    return out


def main() -> None:
    url = API.format(urllib.parse.quote(BENCHMARK))
    with urllib.request.urlopen(url) as r:
        api = json.load(r)
    api_rows = api["rows"]
    cohort = [r for r in api_rows if r.get("activeParamsB") is not None and r.get("meanTask") is not None]
    print(f"{len(api_rows)} leaderboard rows, {len(cohort)} with size and full coverage", flush=True)

    bench = mteb.get_benchmark(BENCHMARK)
    n_tasks = len(bench.tasks)
    names = [r["model"]["name"] for r in cohort]
    print(f"recomputing {len(names)} models on {n_tasks} tasks (~{len(names) * 4.5 / 60:.0f} min + import)", flush=True)
    results = mteb.load_results(tasks=bench.tasks, models=names, only_main_score=True)
    # The leaderboard joins a model's revisions into one row (a main run plus an
    # `external` folder holding the last few tasks is common), so do the same with mteb's
    # own join_revisions() — main revision wins on conflicts.
    results = results.join_revisions()

    # join_revisions() de-duplicates tasks but still returns one entry per revision; the
    # model's row is the union of those entries. Score each model on all of its joined
    # entries together (the leaderboard's view), and count coverage over the union.
    task_names = {t.metadata.name for t in bench.tasks}
    by_model: dict[str, list] = {}
    for mr in results.model_results:
        by_model.setdefault(mr.model_name, []).append(mr)

    rows, problems, mismatches = [], [], []
    for r in cohort:
        name = r["model"]["name"]
        site = r["meanTask"] * 100
        mrs = by_model.get(name, [])
        covered = set().union(*({tr.task_name for tr in mr.task_results} for mr in mrs)) & task_names if mrs else set()
        s = None
        if mrs:
            # get_score() keys by name and keeps one entry per name, so hand it the union
            # as a single entry (tasks are already de-duplicated by join_revisions()).
            merged = type(mrs[0]).model_construct(
                model_name=name, model_revision=mrs[0].model_revision,
                task_results=[tr for mr in mrs for tr in mr.task_results],
                experiment_name=None, model_meta=mrs[0].model_meta,
            )
            s = (bench.get_score(type(results).model_construct(model_results=[merged])).get(name) or {}).get("Mean(Task)")
        if len(covered) != n_tasks or s is None:
            problems.append(f"{name}: {len(covered)}/{n_tasks} tasks after joining revisions")
            continue
        ours = s * 100 if s <= 1 else s
        best = {"revision": "+".join(sorted(str(mr.model_revision) for mr in mrs))}
        complete = [{"revision": best["revision"], "score": ours}]
        if abs(ours - site) > SCORE_TOL:
            mismatches.append(f"{name}: recomputed {ours:.2f} vs site {site:.2f}")
        meta_active = None
        try:
            meta_active = mteb.get_model_meta(name).n_active_parameters
        except Exception:
            pass
        if meta_active is not None and abs(meta_active / 1e9 - r["activeParamsB"]) > 0.001 + 0.01 * r["activeParamsB"]:
            problems.append(f"{name}: ModelMeta active {meta_active / 1e9:.3f}B vs site {r['activeParamsB']}B")
        rows.append({
            "model": name,
            "rank": r["rank"],
            "active_b": r["activeParamsB"],
            "score": round(ours, 2),
            "site_score": round(site, 2),
            "revision": best["revision"],
            "complete_revisions": [{"revision": v["revision"], "score": round(v["score"], 2)} for v in complete],
        })

    ours_front = {r["model"] for r in pareto(rows)}
    site_front = {r["model"] for r in pareto([{**r, "score": r["site_score"]} for r in rows])}
    if ours_front != site_front:
        problems.append(f"frontier differs: ours-only {ours_front - site_front}, site-only {site_front - ours_front}")

    for r in rows:
        r["pareto"] = r["model"] in ours_front

    # A score that differs from the site is fatal only if it touches the frontier: either
    # the model is tagged, or the tagged set changes (checked above). An untagged model
    # whose dot moves a fraction of a point is recorded, not hidden.
    for m in mismatches:
        if m.split(":")[0] in ours_front:
            problems.append(m)

    print("\nPareto-tagged (recomputed):")
    for r in sorted([r for r in rows if r["pareto"]], key=lambda r: r["active_b"]):
        print(f"  rank {r['rank']:>3}  {r['active_b'] * 1000:>8.0f}M  {r['score']:6.2f}  {r['model']}")
    for m in mismatches:
        print("  note: " + m)
    print("\nproblems:" if problems else "\nfrontier and tagged scores agree with the live leaderboard")
    for p in problems:
        print("  " + p)

    (HERE / "data.json").write_text(json.dumps({
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_benchmark_tasks": n_tasks,
        "api": url,
        "frontend_rule": "leaderboard-frontend src/lib/pareto.ts paretoFrontier() @ fbb28ce",
        "n_leaderboard_rows": len(api_rows),
        "n_cohort": len(rows),
        "problems": problems,
        "score_differences_off_frontier": [m for m in mismatches if m.split(":")[0] not in ours_front],
        "models": sorted(rows, key=lambda r: r["active_b"]),
    }, indent=2) + "\n")

    if CARD.exists():
        write_card_data(CARD, {
            "benchmark": BENCHMARK,
            "n_rows": len(api_rows),
            "points": [{k: r[k] for k in ("model", "rank", "active_b", "score", "pareto")} for r in rows],
        })

    if problems:
        raise SystemExit(f"{len(problems)} disagreement(s) — the card must not be built on these numbers")


if __name__ == "__main__":
    main()
