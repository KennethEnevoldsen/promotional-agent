---
id: 2026-07-28-jina-reranker-v35
type: model_addition
trigger: mteb#5041 (no results PR)
trigger_date: 2026-07-28
rejected_on: 2026-08-01
reason: registration and wrapper plumbing only — no results, so no claim to make
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5041
---

## Why it was rejected

PR #5041 registers `ModelMeta` for `jina-reranker-v3.5`, marks v3 as superseded, forwards
a pinned revision through the wrapper, and adapts to a changed `rerank()` signature. No
results PR accompanies it.

Nothing here is a claim about the model's quality — it is registration and plumbing,
which is exactly the kind of minor correction not worth reporting on. Posting "a model
now exists in our registry" with no scores trains followers to ignore the account.

It carries the `new model` label, which is precisely why label-based detection is not
sufficient on its own: the label is accurate but does not imply newsworthiness. The
scanner classified it correctly from the title convention and flagged the missing results
PR, but only a human can decide that this particular registration is not worth waiting on.

## Revisit if

Results are submitted before 2026-08-28, at which point it becomes an ordinary
`model_addition` and a reranker score is worth reporting. Re-running `scan.py` will *not*
resurface it — the trigger PR is recorded here, so the scanner skips it. Move this folder
back to `1-candidates/` by hand if the results land.
