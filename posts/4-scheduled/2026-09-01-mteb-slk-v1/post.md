---
id: 2026-09-01-mteb-slk-v1
type: benchmark_addition
trigger: mteb#4788 (benchmark registration); results#570 (day-one results, same author)
trigger_date: 2026-08-23
scheduled_for: 2026-09-01T14:30:00+02:00
approved_by: kennethenevoldsen (explicit instruction, 2026-08-29)
expires: 2026-09-23
subject: MTEB(slk, v1)
verified: true
evidence: data.json
media: card-1-mteb-slk-v1.png
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/4788
  - https://github.com/embeddings-benchmark/results/pull/570
  - https://arxiv.org/abs/2606.13647
---

```
New benchmark: MTEB(slk, v1) is MTEB's first Slovak board — 31 tasks across 7 task types, 17 built for it: parliamentary sentiment, fact-checking NLI, pharmacy Q&A, news clustering.

Of the 8 models scored on all 31, intfloat/multilingual-e5-large-instruct leads.

Contributed by andrejridzik.
```

## LinkedIn

The Bluesky text plus the one thing 300 characters pushed out: why the board is only
eight models deep today, which otherwise reads as a benchmark nobody has run.

```linkedin
New benchmark: MTEB(slk, v1) is MTEB's first Slovak board — 31 tasks across 7 task types, 17 of them built for it: sentiment in parliamentary debate, fact-checking NLI from Demagog.sk, pharmacist answers to medication questions, news clustering from Pravda.sk and SME.

Of the 8 models scored on all 31 tasks so far, intfloat/multilingual-e5-large-instruct leads at 78.37. Eleven more models are one task short of the board — the ranking will move as they fill in.

Benchmark by andrejridzik, from SkMTEB (arXiv:2606.13647).
```

## The claim

`mteb#4788` registers `MTEB(slk, v1)` — SkMTEB, from arXiv:2606.13647 — as MTEB's first
Slovak benchmark. It is the only benchmark in `mteb/benchmarks/benchmarks/benchmarks.py`
scoped to Slovak; Slovak text appeared before this only inside multilingual tasks, never
as a board.

31 tasks across 7 task types, of which **17 task classes are defined by this PR** (read
off the merged diff and confirmed imported into each package's `__init__.py` — a class
that is defined but never imported is not reachable through `mteb.get_task()`):

| task type | tasks | new in mteb#4788 |
|---|---:|---:|
| Classification | 7 | 3 |
| BitextMining | 6 | 1 |
| Clustering | 5 | 4 |
| Retrieval | 5 | 1 |
| Reranking | 3 | 3 |
| PairClassification | 3 | 3 |
| STS | 2 | 2 |

The other 14 are either Slovak tasks that already existed (`SKQuadRetrieval`,
`SlovakSumRetrieval`, `SlovakHateSpeechClassification.v2`,
`SlovakMovieReviewSentimentClassification.v2`) or multilingual tasks pinned to their
Slovak subsets (`Tatoeba`, `FloresBitextMining`, `NTREXBitextMining`, the two WebFAQ
bitext tasks, `WebFAQRetrieval`, `BelebeleRetrieval`, `SIB200Classification`,
`SIB200ClusteringS2S`, `MultilingualSentimentClassification`).

## The ranking, and why it is stated the way it is

`results#570`, same author, submits results for about twenty models. Eight have all 31
tasks:

| rank | score | size | model |
|---:|---:|---:|---|
| 1 | 78.37 | 560M | `intfloat/multilingual-e5-large-instruct` |
| 2 | 76.00 | 572M | `jinaai/jina-embeddings-v3` |
| 3 | 75.04 | 560M | `intfloat/multilingual-e5-large` |
| 4 | 73.14 | 278M | `intfloat/multilingual-e5-base` |
| 5 | 72.64 | 305M | `Alibaba-NLP/gte-multilingual-base` |

**Eleven more models are short by exactly one task, `WebFAQRetrieval`** — `BAAI/bge-m3`,
`Qwen/Qwen3-Embedding-0.6B`, `google/embeddinggemma-300m`,
`Snowflake/snowflake-arctic-embed-l-v2.0` and others. A ranking over whoever happens to
be complete on a two-day-old board is a fact about submission timing, so `fetch.py`
recomputes the same board with that one task dropped: 18 models qualify, and the leader
and runner-up are unchanged (78.10 and 75.56). `bge-m3` would enter at 3rd.

That check is why the post says "of the 8 models scored on all 31 so far" and not "the
best Slovak model". The leader survives the missing task; the rest of the order does not,
and the post does not claim it.

## What the card shows, and does not

Composition, not ranking: tasks per type, split into new and pre-existing. The day-one
board is deliberately off the card — a card travels as a screenshot without the sentence
that scopes it, and "8 models" needs that sentence. The six highlighted tasks are the
part a reader cannot get from a task count: pharmacist answers to medication questions,
fact-checkers' evidence against political claims, parliamentary sentiment. Those are
Slovak resources, not a translated English board, which is the argument for the benchmark
existing.

## Notes

Credit: andrejridzik, author of both PRs. No Bluesky handle in `social-handles.yaml`, so
plain text, no @-mention. The SkMTEB paper (arXiv:2606.13647) has five authors — named in
the LinkedIn version by way of the citation rather than listed, since the post credits the
contribution to MTEB, and the paper is the reference for the rest.

Breadth (`AGENTS.md` #7): the last three posts were English-language boards
(BRIGHT-Pro, LMEB) and a visual-document one. A Slavic language board with 5M speakers is
the widening this account exists to encourage — and the pharmacy and fact-checking tasks
are domain coverage that the big multilingual boards do not have at all.

`benchmark_task_scores()` was added to `mtebpost/leaderboard_api.py` for the
missing-task check: `benchmark_scores()` drops every row the API gives no aggregate for,
which is exactly the partial-coverage models the check is about.

**Scheduled for 2026-09-01, 14:30+02:00**, approved by kennethenevoldsen on
2026-08-29 ("feel free to schedule all of them now"). Chosen for the Tuesday of the week
after the trigger, ahead of the gemini post on the Thursday, so the two go out two days
apart rather than back to back.
