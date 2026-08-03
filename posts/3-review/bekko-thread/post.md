---
id: bekko-thread
type: model_addition
trigger: mteb#5043 + results#652 (model addition with results)
trigger_date: 2026-07-30
expires: 2026-08-30
subject: hotchpotch/bekko-embedding-v1-a8m
verified: true
evidence: data.json
media: card-1-frontier.png
thread: 2
linkedin: linkedin.md
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5043
  - https://github.com/embeddings-benchmark/results/pull/652
  - https://huggingface.co/hotchpotch/bekko-embedding-v1-a25m
  - https://arxiv.org/abs/2607.25180
---

Post 1 — card: `card-1-frontier.png`

```
New on MTEB: hotchpotch/bekko-embedding-v1-a8m holds 106M parameters but computes just 7.7M per token — the rest is a shared embedding table.

It scores 56.73 on MTEB(Multilingual, v2); a static model of near-identical total size scores 47.21.
```

Post 2 — card: `card-2-tasks.png`

```
Task by task, bekko-embedding-v1-a25m tracks jinaai/jina-embeddings-v3 almost exactly — 58.36 against 58.37 — while computing 12.7x fewer parameters per token.

It gives ground on clustering and wins on bitext mining.
```

## Why a thread rather than two posts

These were drafted as separate candidates and merged. They make one argument in two
moves: the first says what active compute buys against a static baseline, the second
shows that a model 12.7x cheaper per token matches a well-known one *shape for shape*,
not just on average.

Neither is complete alone. The frontier card cannot show that the competence profile
matches; the radar cannot show the size/score trade-off, because it has no size axis. Run
separately they would be two posts about one model in one week, which the cadence rules
push against anyway.

A third draft — `bekko-size-class`, a plain ranking — was dropped. It was the most
legible and least informative of the three, and its rank claim ("top of its size class")
moves as models are added, unlike the frontier and the matched-pair facts.

## Verification

Recomputed from the results repo via `Benchmark.get_score()`, matching the contributor's
PR table exactly.

| Model | Active | Mean(Task) | Coverage |
|---|---:|---:|---:|
| **bekko-embedding-v1-a25m** | 24.9M | **58.36** | 131/131 |
| **bekko-embedding-v1-a8m** | 7.7M | **56.73** | 131/131 |
| jinaai/jina-embeddings-v3 | 316.3M | 58.37 | 131/131 |
| codefuse-ai/F2LLM-v2-80M | 31.6M | 55.23 | 131/131 |
| sentence-transformers/static-similarity-mrl-multilingual-v1 | 0 (static) | 47.21 | 131/131 |

`fetch.py` produces the frontier cohort, `fetch_tasks.py` the per-task-type profile.

## Notes

"Active" versus "total" is load-bearing throughout. a8m is 7.67M active of 105.98M total,
with 98M in a shared embedding table. "A 7.7M model" misleads about memory; "a 106M
model" misleads about compute.

Both cards use the `mteb` package rather than the leaderboard API, deliberately: the
API's `activeParamsB` currently returns total parameters (`issue.md`), and active is the
axis both cards are built on. Do not migrate these two without re-checking that field.

`InstructionReranking` is excluded from the radar — its centered metric goes negative
(-3.34, -4.83) and a negative has no honest position on a zero-based radial axis. MTEB's
own leaderboard drops it for the same reason.

**The Pareto claim is scoped to a cohort** — multilingual models at or below 60M active
parameters with complete coverage — and that qualifier is no longer printed on the card
after decluttering. It survives in the alt text. A screenshot therefore carries the claim
without its scope, which is worth fixing by rewording the subtitle rather than adding a
line back.

Credit: `hotchpotch`. Not tagged — no handle in `social-handles.yaml`.
