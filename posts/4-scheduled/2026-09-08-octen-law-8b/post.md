---
id: 2026-09-08-octen-law-8b
type: model_addition
trigger: mteb#5305 + results#688
trigger_date: 2026-08-26
scheduled_for: 2026-09-08T14:30:00+02:00
approved_by: kennethenevoldsen (explicit instruction, 2026-08-30)
expires: 2026-09-26
subject: litillabs/octen-law-8b-v1
verified: true
evidence: data.json
media: card-1-octen-law-8b.png
competes_with: legal-specialisation
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5305
  - https://github.com/embeddings-benchmark/results/pull/688
  - https://huggingface.co/litillabs/octen-law-8b-v1
---

```
New on MTEB: litillabs/octen-law-8b-v1 takes 1st of 164 on MTEB(Law, v1) at 76.77, 4.19 clear of the next model.

It declares two of the eight tasks as training data. Recomputed without them, the lead widens: 81.77 to 75.00.

Model and results by narcolepticchicken.
```

## LinkedIn

The post plus the caveat that governs every rank on this board and does not fit in 300
characters: who never entered it.

```linkedin
New on MTEB: litillabs/octen-law-8b-v1, a legal-retrieval model adapted from Octen/Octen-Embedding-8B, takes 1st of the 164 models with complete MTEB(Law, v1) results at 76.77 — 4.19 ahead of Hanno-Labs/dinghy-law-8b-v1.

Its own model card declares two of the benchmark's eight tasks, GerDaLIRSmall and LeCaRDv2, as training data. A rank over a board that includes a model's own training set is not a capability claim, so we recomputed the ranking over the six tasks no ranked model declares. The order holds and the margin grows: 81.77 against 75.00. The two declared tasks are among the model's weakest scores, so they are not what puts it on top.

One limit worth stating plainly: 15 of the top 20 models on MTEB(eng, v2) have no complete Law results at all. First here means first among those who entered — which is what any leaderboard rank means, and worth saying out loud on a domain board where entry is self-selecting.

Model and results by narcolepticchicken.
```

## The claim

`mteb#5305` (merged 2026-08-26) registers `litillabs/octen-law-8b-v1` — 7.6B parameters,
dense, English/German/Chinese legal retrieval, `adapted_from` `Octen/Octen-Embedding-8B`.
`results#688`, same author, submits its eight `MTEB(Law, v1)` results the next day.

| rank | score | size | model |
|---:|---:|---:|---|
| **1** | **76.77** | 7.6B | `litillabs/octen-law-8b-v1` |
| 2 | 72.58 | 8.0B | `Hanno-Labs/dinghy-law-8b-v1` |
| 3 | 71.22 | 4.0B | `Hanno-Labs/dinghy-law-4b-v1` |
| 4 | 70.37 | 7.6B | `Mira190/Euler-Legal-Embedding-V1` |
| 5 | 69.33 | 8.0B | `minetta/nemotron-3-embed-8b-legal` |

The 4.19 margin is wider than the gap spanning ranks 2 to 5. The board has moved since
this account last posted it on 2026-08-07: `dinghy-law-4b-v1` led at 71.22 then and is
third now, and 164 models have complete coverage against 159.

## The training-data check, which is the reason this post exists in this shape

The model's own `ModelMeta` declares `GerDaLIRSmall` and `LeCaRDv2` as training data.
**Both are tasks in `MTEB(Law, v1)`.** A rank over a board containing a model's own
training set is not a capability claim, so `fetch.py` recomputes the whole board over the
six tasks that no ranked model declares:

| | published, 8 tasks | 6 undeclared tasks |
|---|---:|---:|
| `litillabs/octen-law-8b-v1` | **76.77** | **81.77** |
| `Hanno-Labs/dinghy-law-8b-v1` | 72.58 | 75.00 |
| margin | 4.19 | 6.77 |

The lead survives and widens. It is not a case of a model being carried by its own
training data: `GerDaLIRSmall` (47.85) and `LeCaRDv2` (75.71) are two of its weakest
eight scores, and dropping them helps it. Dropping `GerDaLIRSmall` is also even-handed
rather than a favour — the `Hanno-Labs/dinghy-law-*` family declares it too.

Both facts are `assert`s in `fetch.py`, not readings off its printout: first on the
published board, and still first on the undeclared-task view.

## What the declarations do not establish

**Of the ten models on the card, only two declare any training data at all.** The
`Hanno-Labs` family names three datasets, this model names three; `Mira190`, `minetta`,
`judicialmind`, both `voyageai` models and `codefuse-ai` declare an empty set or nothing.
So the six-task view is a **lower bound on overlap, not a clean room** — it removes the
overlap that was disclosed, and can say nothing about the labs that disclosed nothing.
The post claims exactly that and no more.

Declared training data is not on the leaderboard API, which reports only whether training
data is open at all, so the declarations are transcribed in `fetch.py` from each model's
`ModelMeta` with its source file named. One transcription trap worth recording:
`codefuse_models.py` names seven of these eight tasks, but in its per-task *instruction*
dictionary, not in `training_datasets` — a grep for the task name would have marked
F2LLM as overlapping when it does not.

## Scope: who never entered

Re-measured for this post rather than carried over from the dinghy-law one: **15 of the
top 20 models on `MTEB(eng, v2)` have no complete `MTEB(Law, v1)` results**, including
the top three overall and `google/gemini-embedding-001`. First here means first among
those who entered. That is what a leaderboard rank always means, and it needs saying on a
domain board, where a legal model has every reason to submit legal results and a frontier
generalist has none. The card carries "164 models with complete results" for the same
reason; the LinkedIn version states the 15 outright.

## What is not claimed

- **No within-family comparison.** The obvious one — this model against the
  `Octen/Octen-Embedding-8B` it was adapted from — is not available: the base model has
  5 of the 8 Law tasks, and its mean over those five (81.16) is not comparable to a mean
  over eight. Tempting and wrong; left out entirely.
- **Nothing about specialisation as a phenomenon.** The same board now shows legal models
  in the top seven and the first general-purpose model 8th, which is a real pattern and a
  different post — it is drafted as `2-drafting/legal-specialisation` and this post is
  marked `competes_with` it. Do not run both in a week.
- **Nothing outside legal retrieval.** The model has 2 of 131 tasks on
  MTEB(Multilingual, v2) and 3 of 21 on RTEB(eng, beta). Its Law results are the whole
  of what can be said about it.

## Notes

**The model id is `litillabs/octen-law-8b-v1`.** `mteb#5305`'s title and body both call
it `narcolepticchicken/octen-law-8b-v1`, but the code it merges registers the `litillabs`
id, which is what the registry, the leaderboard and the `ModelMeta`'s own reference URL
say. Posting the id from the PR title would have named a model that does not exist on the
board.

Credit: narcolepticchicken, author of both PRs. No Bluesky handle in
`social-handles.yaml`, so plain text, no @-mention.

`judicialmind/greenleaf-law-embed-tiny` (`results#684`) landed on the same board in the
same week at 64.49 and 9th, at 596M parameters — the smallest model in the top ten, and
one of only two under a billion. Not this post's subject and not folded into it; worth
remembering if a small-legal-model angle is wanted later.

**Scheduled for 2026-09-08, 14:30+02:00**, approved by kennethenevoldsen on 2026-08-30
("feel free to schedule it"). This is the slot `languagebind-omni` was drafted for before
it was blocked, and it keeps five days between this post and the gemini one on 09-03.
