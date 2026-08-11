---
id: add-dragonkue-multilingual-e5-small
type: model_addition
trigger: mteb#5054 (no results PR)
trigger_date: 2026-07-31
expires: 2026-08-31
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5054
reason: evaluated but not a story: dragonkue/multilingual-e5-small-ko-v2 is rank 16 of 23 on MTEB(kor, v2) at 67.35, +0.22 over its own predecessor. The interesting angle (0.118B within 0.08 of a 9.24B model) repeats 2026-08-05-efficiency-frontier.
rejected_on: 2026-08-07
rejected_by: triage run 2026-08-07 (deepseek-v4-flash), verified by hand
---

## Why this might be a post

Model addition with **no results PR found**. Not postable on its own: a registration without scores is plumbing. Either the results are still coming, or this is metadata-only.

## Before it can move to 2-drafting

- [ ] confirm the pairing above is real (the scanner guesses it from title overlap)
- [ ] check the results are merged and complete, not partial
- [ ] decide the angle, or reject with a reason
