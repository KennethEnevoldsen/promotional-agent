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
"""Evidence for the openness post. Run from the repo root:

    uv run posts/2026-08-10-openness/fetch.py

Slow — roughly 15 minutes. It scores every model in the registry against
MTEB(eng, v2), because the post is a claim about the whole field rather than about one
model, and a sampled field is not a field.

MTEB(eng, v2) is used rather than the multilingual benchmark for one reason: 41 tasks
instead of 131, which is the difference between a load that finishes and one that does
not. It also has the widest model coverage, which matters when the question is "who is
on the board".

Three openness tiers, from `ModelMeta.openness`:

  proprietary   no open weights
  open weights  weights published, but not both training code and training data
  open source   weights + training code + training data — reproducible end to end

The tiers are a simplification of a six-field record (weights, licence, code, data,
paper, model card). "Open source" here means specifically that someone else could
rebuild the model, which is the distinction MTEB cares about and the one that gets
flattened when people say "open".

Coverage is reported alongside the scores, not buried. Requiring complete results drops
the field from 400 models with some results to 99 with all 41 tasks, and the proprietary
tier from 37 to 9 — small enough that "best proprietary model" rests on a handful of
submissions, and notably missing OpenAI and Cohere, whose models are registered and
partially evaluated but never completed. Any claim this post makes about proprietary
models has to survive that.
"""

import json
import pathlib
import warnings
from datetime import date

warnings.filterwarnings("ignore")


import mteb

from mtebpost.cards import write_card_data

BENCHMARK = "MTEB(eng, v2)"
HERE = pathlib.Path(__file__).parent

TIERS = ("proprietary", "open weights", "open source")


def tier_of(meta) -> str:
    if not meta.open_weights:
        return "proprietary"
    o = meta.openness or {}
    if o.get("open training code") and o.get("open training data"):
        return "open source"
    return "open weights"


def main() -> None:
    bench = mteb.get_benchmark(BENCHMARK)
    n_bench = len(bench.tasks)
    metas = {m.name: m for m in mteb.get_model_metas()}

    registered = {t: 0 for t in TIERS}
    for m in metas.values():
        registered[tier_of(m)] += 1

    print(f"scoring {len(metas)} models on {BENCHMARK} ({n_bench} tasks) — this takes ~15 min")
    results = mteb.load_results(tasks=bench.tasks, models=list(metas), only_main_score=True)
    agg = bench.get_score(results)

    # best-covered revision per model; stub revisions carry zero task results
    covered: dict[str, int] = {}
    for mr in results.model_results:
        covered[mr.model_name] = max(covered.get(mr.model_name, 0), len(mr.task_results))

    # "Any results" has to be counted over the keys of `agg`, which is the only place
    # partially-evaluated models survive: load_results filters them out of
    # `model_results`, and get_score gives them Mean(Task)=None. Counting from either of
    # those reports "any" as identical to "complete" and hides the entire funnel — which
    # is exactly the number that tells the reader how thin the proprietary lane is.
    with_any = {t: 0 for t in TIERS}
    for name in agg:
        meta = metas.get(name)
        if meta:
            with_any[tier_of(meta)] += 1

    models = []
    for name, row in agg.items():
        s = row.get("Mean(Task)")
        meta = metas.get(name)
        if s is None or meta is None:
            continue
        t = tier_of(meta)
        if covered.get(name, 0) != n_bench:
            continue  # a mean over a subset is not comparable to a mean over all 41
        models.append({
            "model": name,
            "tier": t,
            "score": round(s * 100, 2) if s <= 1 else round(s, 2),
            "release_date": str(meta.release_date) if meta.release_date else None,
        })

    models.sort(key=lambda r: -r["score"])
    complete = {t: sum(1 for m in models if m["tier"] == t) for t in TIERS}
    best = {t: max((m for m in models if m["tier"] == t), key=lambda m: m["score"], default=None)
            for t in TIERS}

    evidence = {
        "generated": date.today().isoformat(),
        "benchmark": BENCHMARK,
        "n_benchmark_tasks": n_bench,
        "tier_rule": {
            "proprietary": "open_weights is false",
            "open weights": "weights published, but not both training code and data",
            "open source": "weights + training code + training data",
        },
        "coverage": {t: {"registered": registered[t], "any_results": with_any[t],
                         "complete_results": complete[t]} for t in TIERS},
        "models": models,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    card = {
        "benchmark": BENCHMARK,
        "n_tasks": n_bench,
        "tiers": [
            {"tier": t, "n": complete[t], "registered": registered[t],
             "best": best[t]["model"] if best[t] else None,
             "best_score": best[t]["score"] if best[t] else None,
             "scores": [m["score"] for m in models if m["tier"] == t]}
            for t in TIERS
        ],
    }
    write_card_data(HERE / "card.html", card)

    print(f"\n{'tier':<14}{'registered':>11}{'any':>7}{'complete':>10}{'best':>8}")
    for t in TIERS:
        b = best[t]
        print(f"{t:<14}{registered[t]:>11}{with_any[t]:>7}{complete[t]:>10}"
              f"{(b['score'] if b else 0):>8}  {b['model'] if b else '-'}")
    print(f"\nwrote data.json ({len(models)} complete) and card.html data")


if __name__ == "__main__":
    main()
