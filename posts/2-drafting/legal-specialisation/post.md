---
id: legal-specialisation
type: state_of_field
trigger: noticed while drafting dinghy-law-family; no single event
trigger_date: 2026-08-01
expires: 2026-11-01
competes_with: dinghy-law-family
todo:
  - write fetch.py (the query is nearly identical to dinghy-law-family's — reuse it)
  - build a card; the legal/general split is the whole claim, so colour must be decodable
  - widen beyond MTEB(Law, v1) if the claim is about specialisation generally rather than
    about law specifically — one domain is an anecdote
  - resolve the overlap with dinghy-law-family before either is scheduled
---

```
The 5th-best English embedding model ranks 29th on MTEB(Law, v1).

Among models evaluated on both, general ability does not carry over to legal retrieval — the top five on Law are all built for it.
```

## The claim, after correcting for who actually ran the benchmark

**The original framing does not survive.** "Specialists beat generalists" reads as a
claim about capability, but `MTEB(Law, v1)` is not run by the models that would test it:
**14 of the top 20 models on `MTEB(eng, v2)` have no complete Law results at all**,
including the top four overall and `google/gemini-embedding-001`. A legal model has every
reason to submit legal results; a frontier generalist has none. The ranking is shaped by
submission behaviour before it is shaped by ability.

What survives is narrower and still worth saying. Of the six top-20 English models that
*did* run Law, the best manages **rank 6**, and all five specialists beat all six of them:

| eng rank | eng score | Law rank | Law score | model |
|---:|---:|---:|---:|---|
| 5 | 74.75 | **29** | 55.41 | `infgrad/Jasper-Token-Compression-600M` |
| 11 | 73.08 | 6 | 64.66 | `codefuse-ai/F2LLM-v2-14B` |
| 12 | 72.86 | 9 | 63.54 | `codefuse-ai/F2LLM-v2-8B` |
| 13 | 72.41 | 12 | 61.53 | `codefuse-ai/F2LLM-v2-4B` |
| 18 | 71.63 | 15 | 60.32 | `codefuse-ai/F2LLM-v2-1.7B` |
| 19 | 71.41 | 18 | 58.78 | `NovaSearch/jasper_en_vision_language_v1` |

**The strongest line in the table is `Jasper`: 5th on English, 29th on legal.** That is a
*within-model* observation — the same model on two benchmarks — so it is untouched by who
else submitted. Every cross-model ranking here is exposed to the omission bias; that one
is not. It is the honest headline.

For reference, the ranking that prompted this: of 159 models with complete
`MTEB(Law, v1)` results, ranks 1-5 are all legal-domain models and the first
general-purpose model is 6th.

| rank | score | size | model | kind |
|---:|---:|---:|---|---|
| 1 | 71.22 | 4.0B | `Hanno-Labs/dinghy-law-4b-v1` | legal |
| 2 | 70.37 | 7.6B | `Mira190/Euler-Legal-Embedding-V1` | legal |
| 3 | 69.33 | 8.0B | `minetta/nemotron-3-embed-8b-legal` | legal |
| 4 | 65.83 | 0.6B | `Hanno-Labs/dinghy-law-0.6b-v1` | legal |
| 5 | 65.39 | proprietary | `voyageai/voyage-law-2` | legal |
| 6 | 64.66 | 14B | `codefuse-ai/F2LLM-v2-14B` | general |

## Why this is a separate post from `dinghy-law-family`

`dinghy-law-family` announces a model. This makes a claim about the field. They share a
dataset and a chart shape, but the subject is different and so is the risk: a model
announcement is wrong only if the number is wrong, whereas this one is wrong if the
*category* is wrong.

**They compete.** Both are about the same eight rows of the same table, and running them
in the same week would read as one story told twice. Pick one, or merge them into a post
that leads with the model and closes on the pattern — which is probably the strongest
version, but is a third thing rather than either of these.

## What "specialised" means here, and why the name is the right signal

Membership is decided by the model name declaring a legal domain. That sounds weak and is
not: a lab that builds a domain model has every reason to say so in the name, and all
five do.

Checking the metadata confirms the name is in fact the *stronger* signal. Of the five
specialists, **none declares a single legal training dataset** — `Euler-Legal`,
`nemotron-3-embed-8b-legal` and `voyage-law-2` list no training data at all. There is no
metadata flag to prefer here; there is nothing to prefer it to.

The check did sharpen the definition, though. `codefuse-ai/F2LLM-v2-14B` at rank 6 — the
first general-purpose model — *does* list a legal dataset (`Lawzhidao`, one of 152). So
the line is **built for the domain**, not **has seen the domain**. A generalist that
includes legal data among 152 datasets is still a generalist, and the post should say
which of the two it means rather than leaving "specialised" to do the work unaided.

The residual risk is a legal model that does not say so in its name. It is bounded: only
models near the break matter, so it is the top ten or so to check, not 159. Those ten are
checked and the categorisation holds.

**A single benchmark is still thin ground.** If the post is about specialisation
generally, one domain is an anecdote. Checking whether the pattern holds on another domain
benchmark would turn this from an observation into a finding — and if it does not hold,
that is more interesting still.

**What must never be claimed here:** that domain models are better than general models at
legal retrieval. The evidence cannot support it while the four best general models in the
world have not run the benchmark. Everything this post says has to be scoped to models
that were actually evaluated.

## Notes

Data and method are identical to `dinghy-law-family`: leaderboard API, complete coverage
of all 8 tasks, total parameters. See that post's notes for why the API rather than the
package, and why total rather than active.

No contributor credit — this describes no single person's submission. Same open question
as the other state-of-field posts about whether that absence should be explicit.
