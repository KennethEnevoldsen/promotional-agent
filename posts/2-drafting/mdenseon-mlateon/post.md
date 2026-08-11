---
id: mdenseon-mlateon
type: model_addition
trigger_date: 2026-07-30
trigger: mteb#5048 + results#653 (model addition with results)
todo:
  - write fetch.py; the numbers below came from a cross-board lookup during triage and
    must be reproduced through the post's own script before review
  - build the card; the shape is multilingual-vs-English-only on the same two axes
  - decide whether it stands alone or folds into a LightOn/multilingual roundup
expires: 2026-08-30
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5048
  - https://github.com/embeddings-benchmark/results/pull/653
  - https://huggingface.co/blog/lightonai/mDenseOn-mLateOn
  - https://arxiv.org/abs/2607.27178
verified: n/a
media: none
---

```
lightonai/mLateOn and mDenseOn are multilingual extensions of LateOn and DenseOn — eight languages plus English, same backbone.

On BEIR, in English, both beat the English-only models they extend: 23rd of 197 vs 25th, and 28th vs 31st.

Added by NohTow, results by paulomouraj.
```

## The claim

The interesting question about a multilingual extension is what it costs in the original
language. Here the answer is nothing — both multilingual models rank *above* the
English-only versions they derive from, on an English benchmark:

| model | BEIR (of 197) | | CoIR (of 51) | MTEB(Code, v1) (of 45) |
|---|---:|---|---:|---:|
| `lightonai/mLateOn` | **23** (57.56) | vs | 21 (71.26) | 18 (73.48) |
| `lightonai/LateOn` | 25 (57.22) | | — | — |
| `lightonai/mDenseOn` | **28** (56.70) | vs | 25 (69.33) | 19 (71.53) |
| `lightonai/DenseOn` | 31 (56.20) | | — | — |

Both gaps are small — 0.34 and 0.50 points — and the honest framing is "did not cost
anything", not "multilingual training improves English". A third of a point across 15 BEIR
tasks is well inside the range where task selection and run-to-run variance matter, and
the post should not dress it as a gain.

**What makes it worth saying** is that the expected trade-off did not appear. The
assumption a reader brings is that adding eight languages to a fixed-capacity model costs
English performance. On this evidence it did not.

## What must not be claimed

**Not that these are the best multilingual models**, and not anything about their
performance in the eight added languages — no multilingual board here has complete
coverage for them, so the only verified numbers are English ones. A post about
multilingual models that can only cite English results has to say so.

## Notes

Worth noting for eventual selection logic: this PR is unusually careful about train/test
overlap — the contributor lists CodeEditSearch as contaminated even after decontaminating
it, to be conservative. That rigor is on-brand for MTEB and is a candidate angle for a
different sort of post, though it risks reading as singling out one contributor for praise.

Worth noting for the eventual selection logic: this PR is unusually careful about
train/test overlap — the contributor lists CodeEditSearch as contaminated even after
decontaminating it, to be conservative. That kind of rigor is genuinely on-brand for
MTEB and is a candidate angle for a different sort of post, though it risks reading as
singling out one contributor for praise.
