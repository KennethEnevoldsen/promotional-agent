"""Pull benchmark scores and size-peer context out of the MTEB results repo.

Shared by the per-post `fetch.py` scripts. Each post folder keeps its own thin
fetch script naming the exact models, benchmark and peer band it used, so the
provenance of every number in a post is one file away from the post itself.

Two deliberate choices:

* Aggregation goes through `Benchmark.get_score()`, the same path the leaderboard
  uses. We never average task scores by hand — if MTEB changes how a benchmark
  aggregates, these numbers follow automatically instead of quietly diverging.
* Peers are selected by **active** parameters, not total. For models with a large
  shared embedding table the two differ by more than an order of magnitude
  (Bekko a8m: 7.7M active, 106M total), and active is what determines inference
  cost per token.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, asdict

warnings.filterwarnings("ignore")

import mteb  # noqa: E402

MEAN_TASK = "Mean(Task)"


@dataclass
class Entry:
    model: str
    revision: str | None
    score: float  # never None: entries without a score are dropped in scores()
    active_params: int | None
    total_params: int | None
    embedding_params: int | None
    max_tokens: float | None
    n_tasks: int
    n_benchmark_tasks: int

    @property
    def complete(self) -> bool:
        """True when the model was evaluated on every task in the benchmark.

        A mean over a subset of tasks is not comparable to a mean over all of them,
        and MTEB will happily aggregate partial coverage ("Some task results are
        missing. Filling results with None"). Plotting the two side by side would
        invent a comparison that was never run.
        """
        return self.n_tasks == self.n_benchmark_tasks

    @property
    def is_static(self) -> bool:
        """Zero active parameters: a pure lookup table with no transformer layers.

        `0` is a real, meaningful value here, not a missing one. Static embedding models
        (potion, model2vec, static-similarity-mrl) put *every* parameter in the embedding
        table, so `n_parameters - n_embedding_parameters` is genuinely zero. Only `None`
        means unknown.
        """
        return self.active_params == 0

    @property
    def plottable(self) -> bool:
        """Complete coverage and a known size. Zero counts as known."""
        return self.complete and self.active_params is not None

    def as_dict(self) -> dict:
        return {**asdict(self), "complete": self.complete, "plottable": self.plottable}


def size_peers(
    max_active: float,
    min_active: float = 0,
    text_only: bool = True,
    min_languages: int = 1,
) -> list[str]:
    """Model names whose *active* parameter count falls in [min_active, max_active].

    `min_languages` exists because a peer set is a claim about who was competing.
    On a multilingual benchmark, an English-only model scores low because it was never
    built for the task — including it both flatters the subject and implies the peer is
    worse than it is. Set it above 1 whenever the benchmark is multilingual.

    Note that `min_active=0` genuinely includes static embedding models, whose active
    count is zero rather than missing. They belong in a size cohort — they are the
    limiting case of "put the parameters in the embedding table".
    """
    out = []
    for m in mteb.get_model_metas():
        n = m.n_active_parameters
        if n is None or not (min_active <= n <= max_active):
            continue
        if text_only:
            mods = [str(x) for x in (m.modalities or [])]
            if mods and "text" not in mods:
                continue
        if min_languages > 1 and len(m.languages or []) < min_languages:
            continue
        out.append(m.name)
    return out


def scores(benchmark: str, models: list[str]) -> list[Entry]:
    """Aggregated benchmark score per model, joined with size metadata.

    Models with no results on this benchmark are dropped rather than reported as
    zero — a missing evaluation is not a bad score, and conflating the two is how
    a chart ends up defaming a model that was simply never run.
    """
    bench = mteb.get_benchmark(benchmark)
    n_bench_tasks = len(bench.tasks)
    results = mteb.load_results(tasks=bench.tasks, models=models, only_main_score=True)
    agg = bench.get_score(results)

    # A model appears once per *revision*, and stub revisions (e.g. "external") carry
    # zero task results. Keeping the last one seen silently reports 0 tasks for a model
    # that was in fact fully evaluated — so take the best-covered revision per model.
    best: dict[str, tuple[int, str | None]] = {}
    for mr in results.model_results:
        n = len(mr.task_results)
        if n > best.get(mr.model_name, (-1, None))[0]:
            best[mr.model_name] = (n, mr.model_revision)

    out = []
    for name, row in agg.items():
        score = row.get(MEAN_TASK)
        if score is None:
            continue
        try:
            meta = mteb.get_model_meta(name)
        except Exception:
            meta = None
        n_tasks, revision = best.get(name, (0, None))
        active = getattr(meta, "n_active_parameters", None)
        out.append(
            Entry(
                model=name,
                revision=revision,
                score=round(score * 100, 2) if score <= 1 else round(score, 2),
                # 0 is a real value (static embedding models); only None is unknown
                active_params=active,
                total_params=getattr(meta, "n_parameters", None) or None,
                embedding_params=getattr(meta, "n_embedding_parameters", None),
                max_tokens=getattr(meta, "max_tokens", None),
                n_tasks=n_tasks,
                n_benchmark_tasks=n_bench_tasks,
            )
        )
    return sorted(out, key=lambda e: e.score, reverse=True)


def rank_of(entries: list[Entry], model: str) -> tuple[int, int]:
    """1-indexed rank of `model` within `entries`, and the cohort size."""
    ordered = sorted(entries, key=lambda e: e.score, reverse=True)
    for i, e in enumerate(ordered, 1):
        if e.model == model:
            return i, len(ordered)
    raise KeyError(f"{model} not in cohort")
