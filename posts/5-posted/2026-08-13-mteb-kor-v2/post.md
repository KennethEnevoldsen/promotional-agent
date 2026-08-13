---
id: 2026-08-13-mteb-kor-v2
type: benchmark_addition
trigger: mteb#4870 (merged 2026-07-31)
trigger_date: 2026-07-31
approved_by: kennethenevoldsen (explicit instruction, 2026-08-12)
scheduled_for: 2026-08-13T14:30:00+02:00
expires: 2026-09-30
subject: MTEB(kor, v2)
verified: true
evidence: data.json
media: card.png
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/4870
posted_on: 2026-08-13
url: https://bsky.app/profile/mteb.org/post/3msxrah6mia2y
---

```
New benchmark: MTEB(kor, v2) is now the default Korean board, superseding the 6-task v1.

20 tasks across 6 task types, adding clustering and NLI and with an increased focus on retrieval.

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

## Does the broader benchmark change who's best?

The same size-bucket Pareto the leaderboard page itself shows — best model in `>5B`,
`1-5B`, `500M-1B`, `<500M` — under v1's scoring and under v2's. Score is not the point
here; identity is.

**Restricted to the 23 models with complete coverage on both boards.** An earlier version
of this compared each board's own independent leader and got a false-looking "change" in
one bucket: the v1 leader there had scores for only 8 of v2's 20 tasks — it never ran
clustering or NLI at all — so it dropped out of the v2 ranking for lack of coverage, not
for losing. Since v2's task set is a superset of v1's, complete v2 coverage already implies
complete v1 coverage, so restricting to models scored on both isn't a smaller, different
sample — it's exactly the 23 models with complete v2 coverage, compared fairly on both
scales.

| bucket | n | v1 leader | v2 leader | changed? |
|---|---:|---|---|:---:|
| >5B | 4 | `Qwen/Qwen3-Embedding-8B` (77.86) | `Qwen/Qwen3-Embedding-8B` (77.73) | no |
| 1-5B | 3 | `Qwen/Qwen3-Embedding-4B` (77.44) | `Qwen/Qwen3-Embedding-4B` (76.94) | no |
| 500M-1B | 7 | `nlpai-lab/KURE-v1` (74.27) | `codefuse-ai/F2LLM-v2-0.6B` (72.16) | **yes** |
| <500M | 9 | `hotchpotch/bekko-embedding-v1-a25m` (69.80) | `hotchpotch/bekko-embedding-v1-a25m` (67.86) | no |

Three of four keep the same leader under a benchmark with more than three times the tasks
and two new task types — the old, narrower board was not misleading about those three
classes. The 500M-1B class genuinely reorders: `KURE-v1` led under v1's six tasks,
`F2LLM-v2-0.6B` leads once clustering, NLI and the wider retrieval set are added — and
because both ran the full task list on both boards, this is a real capability difference,
not a coverage artifact.

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
