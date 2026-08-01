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
"""Per-task-type scores for the Bekko radar card. Run from the repo root:

    uv run posts/2026-08-09-bekko-task-profile/fetch.py

The scatter and bar cards plot one number per model. This one opens that number up:
`Benchmark.get_score()` returns a score per task type, which is what the radar draws.

The radar answers a different question from the other two cards, so it is built
differently: **one subject against references**, not a ranking. The subject is
`bekko-embedding-v1-a25m`; the comparison that carries the post is
`jinaai/jina-embeddings-v3`, which scores 58.37 to Bekko's 58.36 — a gap of 0.01 — while
computing 12.7x more per token. That pair is the story, so jina is highlighted and the
remaining references are drawn as grey context.

Only the a25m variant appears. Two Bekko lines on the same radar sit almost on top of
each other and add nothing: the size/score trade is the scatter card's job.

InstructionReranking is excluded. Its metric is centered and can go negative, and a
negative has no honest position on a radial axis that starts at zero. MTEB's own
leaderboard drops it from its radar for the same reason — see the comment in
`mteb/leaderboard/figures.py`: "Not displayed, because the scores are negative, doesn't
work well with the radar chart."
"""

import json
import pathlib
import warnings

warnings.filterwarnings("ignore")


import mteb

from mtebpost.cards import write_card_data

BENCHMARK = "MTEB(Multilingual, v2)"
SUBJECT = "hotchpotch/bekko-embedding-v1-a25m"
HIGHLIGHT = "jinaai/jina-embeddings-v3"     # near-identical score, far larger
REFERENCES = [
    "intfloat/multilingual-e5-large-instruct",
    "codefuse-ai/F2LLM-v2-80M",
    "ibm-granite/granite-embedding-97m-multilingual-r2",
]

EXCLUDE_AXES = {"InstructionReranking"}
NOT_AXES = {"Mean(Task)", "Mean(TaskType)", "Rank"}

HERE = pathlib.Path(__file__).parent


def main() -> None:
    bench = mteb.get_benchmark(BENCHMARK)
    models = [SUBJECT, HIGHLIGHT] + REFERENCES
    results = mteb.load_results(tasks=bench.tasks, models=models, only_main_score=True)
    agg = bench.get_score(results)

    counts: dict[str, int] = {}
    for t in bench.tasks:
        tt = getattr(t.metadata, "type", None)
        if tt:
            counts[str(tt)] = counts.get(str(tt), 0) + 1

    axes = [
        k for k in agg[SUBJECT]
        if k not in NOT_AXES and k not in EXCLUDE_AXES and agg[SUBJECT][k] is not None
    ]
    axes.sort(key=lambda k: -counts.get(k, 0))  # busiest task type first, clockwise

    def pct(v):
        return round(v * 100, 2) if v is not None and v <= 1 else (round(v, 2) if v else None)

    series = []
    for name in models:
        row = agg.get(name, {})
        meta = mteb.get_model_meta(name)
        series.append({
            "model": name,
            "role": "subject" if name == SUBJECT else "highlight" if name == HIGHLIGHT else "reference",
            "active": meta.n_active_parameters,
            "total": meta.n_parameters,
            "mean": pct(row.get("Mean(Task)")),
            "values": [pct(row.get(a)) for a in axes],
        })

    sub = next(s for s in series if s["role"] == "subject")
    hi = next(s for s in series if s["role"] == "highlight")

    card = {
        "benchmark": BENCHMARK,
        "n_tasks": len(bench.tasks),
        "axes": [{"name": a, "n_tasks": counts.get(a)} for a in axes],
        "excluded_axes": sorted(EXCLUDE_AXES),
        "shrink_factor": round(hi["active"] / sub["active"], 1),
        "score_gap": round(abs(hi["mean"] - sub["mean"]), 2),
        "series": series,
    }
    write_card_data(HERE / "card.html", card)

    print(f"axes ({len(axes)}): " + ", ".join(f"{a} ({counts.get(a)})" for a in axes))
    print(f"excluded: {', '.join(sorted(EXCLUDE_AXES))}")
    for s in series:
        print(f"  {s['role']:<10} {s['mean']:>6}  {s['active']/1e6:>7.1f}M active  {s['model']}")
    print(f"\n{sub['model']} vs {hi['model']}: "
          f"{card['score_gap']} apart, {card['shrink_factor']}x fewer active params")
    print(json.dumps({"wrote": str(HERE / "card.html")}))


if __name__ == "__main__":
    main()
