---
id: mdenseon-mlateon
type: model_addition
trigger_date: 2026-07-30
trigger: mteb#5048 + results#653 (model addition with results)
todo:
  - results are merged (#653) but the scores have never been recomputed here
  - no fetch.py and no card; the draft states no numbers at all
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
lightonai/mDenseOn and lightonai/mLateOn are now in MTEB — multilingual extensions of DenseOn and LateOn.

Trained with translate-train across eight languages plus English, on an mmBERT-base backbone with 8k context. Dense and late-interaction variants.

Added by NohTow, results by paulomouraj.
```

## Notes

Results did land (#653), so this could carry numbers — I have not pulled them, so the
draft deliberately states none rather than guessing. Either verify and upgrade this to
the scored template, or run it as-is.

Worth noting for the eventual selection logic: this PR is unusually careful about
train/test overlap — the contributor lists CodeEditSearch as contaminated even after
decontaminating it, to be conservative. That kind of rigor is genuinely on-brand for
MTEB and is a candidate angle for a different sort of post, though it risks reading as
singling out one contributor for praise.
