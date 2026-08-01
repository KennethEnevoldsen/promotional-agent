---
id: bekko-task-profile
type: model_addition
trigger_date: 2026-07-30
trigger: mteb#5043 + results#652 (model addition with results)
expires: 2026-08-30
subject: hotchpotch/bekko-embedding-v1-a25m
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5043
  - https://github.com/embeddings-benchmark/results/pull/652
verified: true
evidence: card.html (#card-data)
media: card.png
alt: card.txt
---

```
hotchpotch/bekko-embedding-v1-a25m matches jinaai/jina-embeddings-v3 on MTEB(Multilingual, v2) — 58.36 against 58.37 — while computing 12.7x fewer parameters per token.

Task by task, the two profiles nearly overlap.
```

## The angle

The sharpest single fact in the Bekko material, and the only card that can show it:
**two models a hundredth of a point apart, one of them 12.7x cheaper per token.** A
ranking would put them adjacent and say nothing; a size axis would show the gap but not
that the *shape* of their competence matches.

Where they differ is legible too: Bekko is ahead on BitextMining and PairClassification,
jina-v3 slightly ahead on STS and Clustering.

## Why it is built differently

One subject against references, not a ranking. The subject is brand blue, the one
comparison worth naming is brand purple, and the remaining three models are grey context
— roles rather than categories, so the eye goes to the pair the post is about.

Only the a25m variant appears. Two Bekko lines sit almost on top of each other and add
nothing; the size/score trade is the frontier post's job.

The subtitle is generated from the data rather than written by hand, so it cannot drift
if either score moves.

## InstructionReranking is excluded

Its metric is centered and can go negative — Bekko scores -3.34 and -4.83 — and a
negative has no honest position on a radial axis that starts at zero. Clamping it to the
centre would draw a score nobody achieved.

MTEB's own leaderboard drops it from its radar for the same reason. From
`mteb/leaderboard/figures.py`:

> Not displayed, because the scores are negative, doesn't work well with the radar chart.

Eight task types remain, `fetch.py` records the exclusion, and the alt text states it.

## Verification

| Model | Active | Mean(Task) |
|---|---:|---:|
| **hotchpotch/bekko-embedding-v1-a25m** | 24.9M | **58.36** |
| jinaai/jina-embeddings-v3 *(highlighted)* | 316.3M | 58.37 |
| intfloat/multilingual-e5-large-instruct | 304.0M | 63.22 |
| codefuse-ai/F2LLM-v2-80M | 31.6M | 55.23 |
| ibm-granite/granite-embedding-97m-multilingual-r2 | 28.3M | 51.92 |

Per-task-type scores come from `Benchmark.get_score()` and are written into
`card.html`'s `#card-data` block by `fetch.py`.

## Notes

`multilingual-e5-large-instruct` outscores both at 63.22 and is drawn as grey context.
That is deliberate — it is not the comparison the post is making — but it does mean the
card shows a model beating the subject without remarking on it. Honest, and worth being
comfortable with before posting.
