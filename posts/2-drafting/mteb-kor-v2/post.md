---
id: mteb-kor-v2
type: benchmark_addition
trigger: mteb#4870 (merged 2026-07-31)
trigger_date: 2026-07-31
expires: 2026-09-30
subject: MTEB(kor, v2)
todo:
  - write fetch.py; numbers below came from a cross-board lookup during triage and must be
    reproduced through the post's own script before review
  - build the card; the shape is v1 vs v2 by task type, not a model ranking
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/4870
verified: true
media: none
---

```
New benchmark: MTEB(kor, v2) is now the default Korean board, superseding the 6-task v1.

20 tasks across 6 task types. Clustering and NLI are both new — Korean models were never scored on either here before.

Added by daegonYu.
```

## The claim

`mteb#4870` creates `MTEB(kor, v2)` and marks `MTEB(kor, v1)` superseded. The bare
`MTEB(kor)` alias moves to v2, and the leaderboard menu now shows v2 by default, so this
is a replacement rather than an addition alongside.

| | v1 | v2 |
|---|---:|---:|
| tasks | 6 | **20** |
| task types | 4 | **6** |
| models with complete coverage | 116 | 23 |

v2 contains all six of v1's tasks, so it is a strict superset — no model's existing work is
invalidated, and the two boards are directly comparable at the task level.

**The two new task types are the substance.** v1 covered retrieval, reranking,
classification and STS. v2 adds:

- **clustering** — `SIB200ClusteringS2S`, `KlueMrcDomainClustering`,
  `KlueYnatMrcCategoryClustering`
- **pair classification / NLI** — `KLUE-NLI`, `KorNLI`, `PawsXPairClassification`

Retrieval also widens considerably, from `MIRACLRetrieval` and `Ko-StrategyQA` to include
`LawIRKo`, `SQuADKorV1Retrieval`, `AutoRAGRetrieval`, `PublicHealthQA`,
`BelebeleRetrieval`, `MultiLongDocRetrieval` and `MrTidyRetrieval`.

## The completeness figure cuts the other way, and that is fine

Only 23 models have complete v2 coverage against 116 on v1. That is not a regression —
20 tasks is a higher bar than 6, and a board that is easy to complete is not measuring
much. Worth stating plainly rather than hiding, since anyone comparing the two boards will
notice the model count dropped.

## Registered alongside it

The same PR adds `ModelMeta` for nine Korean community models that already had results but
no registry entry, so their scores existed and did not render. Six now have complete v2
coverage:

| rank | score | model |
|---:|---:|---|
| 8 | 71.95 | `nlpai-lab/KURE-v1` |
| 9 | 71.63 | `dragonkue/snowflake-arctic-embed-l-v2.0-ko` |
| 10 | 71.29 | `telepix/PIXIE-Rune-v1.5` |
| 11 | 70.87 | `dragonkue/BGE-m3-ko` |
| 12 | 70.38 | `nlpai-lab/KoE5` |
| 18 | 67.13 | `dragonkue/multilingual-e5-small-ko` |

The other three — `exp-models/dragonkue-KoEn-E5-Tiny`, `jhgan/ko-sroberta-multitask`,
`upskyy/bge-m3-korean` — have no complete v2 coverage and are not claimed here.

This is good material but it is the second story, not the first. A new default benchmark
for a language is the announcement; who appears on it is what the next post is about.

## What must not be claimed

**Not that `MTEB(kor, v1)` grew from 6 tasks to 19.** The PR body says exactly that and
both halves are wrong: v1 is unchanged at 6 tasks on the live board, and the new suite has
20, not 19. The contributor was describing intent, not the merged result. A PR author's
summary of their own PR is a claim to check, never a fact to repeat — `AGENTS.md` #3.

## The other story in this data

The top seven models on `MTEB(kor, v2)` are general-purpose multilingual models —
`Qwen/Qwen3-Embedding-8B` leads at 77.73, then the `codefuse-ai/F2LLM-v2` family. The best
Korean-specialised model is 8th.

That is the mirror image of what `legal-specialisation` found on `MTEB(Law, v1)`, where
specialists take the top five. Two domains, opposite answers — a far stronger post than
either alone, and the second domain that draft says it needs. Flagged there; deliberately
not spent here.

## Notes

Added by daegonYu. No Bluesky handle on file, so credit is plain text.
