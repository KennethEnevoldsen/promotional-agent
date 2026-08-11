---
id: modelmeta-minetta-nemotron-3-embed
type: model_addition
trigger: mteb#5027 + results#640
trigger_date: 2026-07-26
expires: 2026-08-26
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5027
  - https://github.com/embeddings-benchmark/results/pull/640
reason: evaluated but not a story: rank 4 of 160 on MTEB(Law, v1) at 69.33, and the account published a MTEB(Law, v1) post on 2026-08-07. A second legal post for a non-headline rank would tell the same story twice.
rejected_on: 2026-08-07
rejected_by: triage run 2026-08-07 (deepseek-v4-flash), verified by hand
---

## Why this might be a post

Model addition with a matching results PR — the most reliable trigger there is. Worth a post if the scores say something a reader could not guess from the model card.

## Before it can move to 2-drafting

- [ ] confirm the pairing above is real (the scanner guesses it from title overlap)
- [ ] check the results are merged and complete, not partial
- [ ] decide the angle, or reject with a reason
