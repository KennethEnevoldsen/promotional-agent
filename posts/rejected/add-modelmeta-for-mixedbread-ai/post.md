---
id: add-modelmeta-for-mixedbread-ai
type: model_addition
trigger: mteb#5044 + results#655
trigger_date: 2026-07-29
expires: 2026-08-29
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5044
  - https://github.com/embeddings-benchmark/results/pull/655
reason: evaluated but not a story: the merged results (results#655) are MTEB(eng, v2), where the model is rank 76 of 180. The MTEB(deu, v1) results the PR body points at (results#647) were closed, never merged.
rejected_on: 2026-08-07
rejected_by: triage run 2026-08-07 (deepseek-v4-flash), verified by hand
---

## Why this might be a post

Model addition with a matching results PR — the most reliable trigger there is. Worth a post if the scores say something a reader could not guess from the model card.

## Before it can move to 2-drafting

- [ ] confirm the pairing above is real (the scanner guesses it from title overlap)
- [ ] check the results are merged and complete, not partial
- [ ] decide the angle, or reject with a reason
