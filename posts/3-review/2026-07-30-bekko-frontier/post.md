---
id: 2026-07-30-bekko-frontier
type: model_addition
trigger_date: 2026-07-30
trigger: mteb#5043 + results#652 (model addition with results)
expires: 2026-08-30
subject: hotchpotch/bekko-embedding-v1-a8m
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5043
  - https://github.com/embeddings-benchmark/results/pull/652
  - https://huggingface.co/hotchpotch/bekko-embedding-v1-a25m
  - https://arxiv.org/abs/2607.25180
verified: true
evidence: data.json
media: card.png
alt: card.txt
---

```
New on MTEB: hotchpotch/bekko-embedding-v1-a8m holds 106M parameters but computes just 7.7M per token — the rest is a shared embedding table.

It scores 56.73 on MTEB(Multilingual, v2); a static model of near-identical total size scores 47.21.
```

## The angle

**What active compute buys.** `static-similarity-mrl-multilingual-v1` holds 108.4M
parameters and computes **none** of them per token — a pure lookup table — and reaches
47.21. Bekko a8m holds 106.0M, a near-identical total, computes 7.7M of them, and
reaches 56.73. Roughly nine points for a small amount of per-token compute, at the same
memory footprint.

The card draws the Pareto frontier, and three models sit on it: the static baseline at
one end, then both Bekko variants. Nothing in this cohort is smaller *and* higher
scoring. That is more checkable than a rank, because it does not depend on how many
models happen to be in the cohort — and it is a staircase rather than a diagonal, so it
never implies a result at a size nobody trained.

## Verification

Recomputed from the results repo via `Benchmark.get_score()`, matching the contributor's
PR table exactly.

| Model | Active | Mean(Task) | Coverage |
|---|---:|---:|---:|
| **bekko-embedding-v1-a25m** | 24.9M | **58.36** | 131/131 |
| **bekko-embedding-v1-a8m** | 7.7M | **56.73** | 131/131 |
| codefuse-ai/F2LLM-v2-80M | 31.6M | 55.23 | 131/131 |
| ibm-granite/granite-embedding-97m-multilingual-r2 | 28.3M | 51.92 | 131/131 |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 21.6M | 48.73 | 131/131 |
| sentence-transformers/static-similarity-mrl-multilingual-v1 | 0 (static) | 47.21 | 131/131 |

## Notes

"Active" versus "total" is load-bearing and stated explicitly. a8m is 7.67M active of
105.98M total, with 98M in the shared embedding table. "A 7.7M model" misleads about
memory; "a 106M model" misleads about compute.

**The subtitle is a claim, not a description** — "a new Pareto frontier for
parameter-efficient multilingual embeddings". True of the cohort in `data.json`, but the
cohort statement is no longer printed on the card (it reaches the alt text only), so a
screenshot carries the claim without its scope. Either reword the subtitle to bound
itself or accept that. Re-run `fetch.py` before posting: this is the one claim that goes
stale if the leaderboard moves.

**On the cohort.** Multilingual text models at or below 60M active parameters with
complete coverage of all 131 tasks. Three filters matter:

- *Multilingual only* — without it the cohort picks up e5-small-v2, bge-small-en-v1.5
  and all-MiniLM-L6-v2, English-only models scoring 41-45 on a multilingual benchmark.
  Keeping them would widen Bekko's margin *and* imply three well-regarded models are
  worse than they are.
- *Complete coverage only* — MTEB aggregates partial results without complaining, and a
  mean over a subset is not comparable to a mean over all 131.
- *Static models included* — an earlier cohort dropped them by treating
  `n_active_parameters == 0` as missing. It is a real value, and dropping it deleted the
  single most informative peer.

The 60M boundary is a judgement call and the one input a reader cannot check. It lives
in `fetch.py` so it is at least inspectable.

**Open:** `F2LLM-v2-80M` is named "80M" but registers 31.6M active, and is the closest
competitor at 55.23. Worth confirming before the post leans on the size comparison.
