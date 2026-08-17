---
id: 2026-08-20-most-embed-de
type: model_addition
trigger: mteb#5149 + results#675
trigger_date: 2026-08-11
scheduled_for: 2026-08-20T14:30:00+02:00
approved_by: kennethenevoldsen (explicit instruction, 2026-08-17)
expires: 2026-09-11
verified: true
media: card-1-most-embed-de.png
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5149
  - https://github.com/embeddings-benchmark/results/pull/675
---

```
New on MTEB: malteos/most-embed-de, a German retrieval model fine-tuned from Nemotron-3-Embed-1B, takes 1st of 106 models with full coverage on a custom 6-task German-retrieval subset at 58.07 — beating the runner-up at roughly 1/15th the active parameters.
```

## Why this is a post

Model addition with a matching results PR, pairing confirmed real (results#675's body
names mteb#5149's exact revision). `malteos/most-embed-de` — 1.1B parameters, German
retrieval, fine-tuned from `nvidia/Nemotron-3-Embed-1B-BF16` — is the template's first
real test case: this file exists to work through
[`mtebpost/model_release.py`](/src/mtebpost/model_release.py) end to end, not just
because the model is unusually notable.

**Coverage is 6 tasks, not a registered benchmark.** results#675 has exactly 6 results:
`GerDaLIR`, `GerDaLIRSmall`, `GermanDPR`, `GermanQuAD-Retrieval`, `MIRACLReranking`,
`XMarket` — a German-retrieval slice, not full `MTEB(deu, v1)` (19 tasks, including
classification/clustering/STS the model was never run on). The claim has to be scoped
to "German retrieval" using exactly those 6 tasks (`mtebpost.model_release.cohort()`
with an explicit task list), not stretched to a 19-task board it has no results on.
`XMarket` and `MIRACLReranking` are themselves multi-language — pinned to their "de"
subset (`subsets=` in `fetch.py`), the same scoping the registered `MTEB(deu, v1)`
benchmark itself uses for these two tasks.

**There is a named comparison candidate, not just a nearest score.** The PR body says
plainly: "mirrors the base model's entry exactly, so results are directly comparable
with the Nemotron-3-Embed baseline" — `adapted_from="nvidia/Nemotron-3-Embed-1B-BF16"`
in the `ModelMeta`. Checked directly in `fetch.py`, since `recommend_chart()` cannot see
that a specific model is *the* comparison rather than just the closest score.

## What fetch.py found

Ran against the live leaderboard-backend API (`mtebpost/leaderboard_api.py`), not the
local `mteb` library — the local package is pinned to a 2026-07-30 release
(`pyproject.toml`'s `exclude-newer`) and has no `ModelMeta` for this model at all
(registered 2026-08-11). See `docs/card-design.md`'s "model-release template" section.

- **`malteos/most-embed-de` scores 58.07** on the 6-task German-retrieval subset —
  **highest of 106 models with full coverage of the same 6 tasks**, ahead of
  `codefuse-ai/F2LLM-v2-14B` (55.73, 13.2B active — ~15× the size) and everything else
  in the cohort, including `GritLM/GritLM-7B`, `intfloat/e5-mistral-7b-instruct`, and
  every `multilingual-e5-large` variant.
- `nvidia/Nemotron-3-Embed-1B-BF16` (the base model) has only 5/6 tasks (missing
  `GerDaLIRSmall`) — 58.35 on those 5, essentially tied with the subject task-for-task
  (e.g. `GerDaLIR`: 0.2965 vs 0.2952). Real and worth a mention, but not a clean
  same-scope comparison, and it doesn't change which chart tells the stronger story.
- `recommend_chart()` picked **pareto** — non-dominated at *any* size in the cohort, not
  just within a size band. Drafted at `card-1-most-embed-de.html`/`.png`.
- `mteb/baseline-bm25s` (lexical baseline, not a trained model) also sits in the cohort
  at 44.8 — worth a decision before scheduling: keep it as a reference point (arguably
  informative — a strong non-neural baseline is itself a fact worth knowing) or drop it
  from the peer count as not a real "model" comparison.

## Notes

**`mteb/baseline-bm25s` stays in the cohort.** It sits at 44.8, well below the subject's
58.07 — it does not touch the "highest of 106" or "non-dominated at any size" claims
either way, and `data.json` keeping every qualifying model (CONTRIBUTING.md) is worth
more than trimming a non-neural reference point that isn't doing any work either way.

**The `Nemotron-3-Embed-1B-BF16` base-model tie is real but left out of the post text.**
It only has 5/6 tasks (missing `GerDaLIRSmall`), so 58.35 there isn't the same
comparison as the subject's 6-task 58.07 — close per-task (`GerDaLIR`: 0.2965 vs
0.2952) but not a clean single number to state next to the headline claim, and the
"1st of 106" finding is the stronger, cleaner story on its own. Worth keeping in mind
if this doesn't survive review and a fallback angle is needed.
