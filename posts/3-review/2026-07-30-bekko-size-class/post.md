---
id: 2026-07-30-bekko-size-class
type: model_addition
trigger_date: 2026-07-30
trigger: mteb#5043 + results#652 (model addition with results)
expires: 2026-08-30
subject: hotchpotch/bekko-embedding-v1-a25m
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5043
  - https://github.com/embeddings-benchmark/results/pull/652
verified: true
evidence: data.json
media: card.png
alt: card.txt
---

```
Bekko tops its size class on MTEB(Multilingual, v2).

Among multilingual models under 60M active parameters, hotchpotch/bekko-embedding-v1-a25m leads at 58.36 and the 7.7M-active a8m is second at 56.73.
```

## The angle

The plainest of the three: **who is ahead, and by how much.** No second axis to parse,
no shape to interpret — a ranking with the numbers printed.

It is also the least informative, and the card admits it. Size is demoted to a caption
under each name, so "top of its size class" rests on the subtitle rather than on
anything visible in the bars. That is the trade: legibility for the dimension that makes
the result interesting.

## Two decisions

**Bars start at zero.** The Arena reference this borrows from truncates its Elo axis at
1,450, which is conventional for Elo but would misstate a 47-vs-58 gap on a 0-100 scale
as far larger than it is. The cost is a less dramatic chart; ordering and printed values
carry the detail instead.

**`Qwen/Qwen3-Embedding-8B` sits above the ranking, hatched.** It is ~280x over the size
cap, so ranking it against the cohort would be exactly the unfair comparison the cohort
filter exists to prevent. But without it a reader has no way to know whether 58 is good
in absolute terms — it is a good score *for 25M active parameters*, and the reference is
what makes that legible. The hatch marks it as a different kind of thing rather than a
competitor, and it is unnumbered and separated by a rule.

## Verification

Same cohort and same numbers as the frontier post — see `data.json`, produced by
`fetch.py`. Recomputed from the results repo via `Benchmark.get_score()`.

| | Active | Mean(Task) |
|---|---:|---:|
| Qwen/Qwen3-Embedding-8B *(reference)* | 6.9B | 70.58 |
| **bekko-embedding-v1-a25m** | 24.9M | **58.36** |
| **bekko-embedding-v1-a8m** | 7.7M | **56.73** |
| codefuse-ai/F2LLM-v2-80M | 31.6M | 55.23 |
| ibm-granite/granite-embedding-97m-multilingual-r2 | 28.3M | 51.92 |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 21.6M | 48.73 |
| sentence-transformers/static-similarity-mrl-multilingual-v1 | static | 47.21 |

## Notes

The rank claim lives in the text here, unlike the frontier post which deliberately
avoids one. It is true of this cohort today and it will move as models are added — which
is the reason the frontier framing is the more durable of the two. If only one Bekko post
runs, run that one.
