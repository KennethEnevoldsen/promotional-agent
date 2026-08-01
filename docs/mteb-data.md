# Working with the MTEB API

Facts that cost time to discover and are not recoverable by reading the code.

## The parts that surprise

- **The results repo is cached at `~/.cache/mteb/remote`** (~3.1 GB, 659 model dirs).
  `mteb.load_results()` pulls the latest into it.
- **`load_results()` over all models is far too slow** — loading all 659 models across
  the 131 tasks of `MTEB(Multilingual, v2)` did not finish in 10 minutes. *Always* pass
  a `models=` filter. Select the cohort first from `mteb.get_model_metas()`, which is
  in-memory and instant, then load results only for those names.
- **Aggregate with `Benchmark.get_score(results)`**, never by averaging task scores by
  hand. It is the same path the leaderboard uses and returns `{"Mean(Task)": …,
  "Mean(TaskType)": …}` per model.
- **`n_active_parameters` vs `n_parameters` matters enormously.** Bekko a8m is 7.7M
  active but 106M total — 98M sit in a shared multilingual embedding table. Active is
  what drives per-token inference cost and is the right axis for size comparisons.
- `mteb.get_model_meta(name)` also carries `max_tokens`, `embed_dim`, `languages`,
  `release_date`, `training_datasets`, `zero_shot_percentage`.
- Importing `mteb` emits a wall of beta-task warnings on stderr. Filter with
  `warnings.filterwarnings("ignore")` and grep out the rest.

### Three traps that silently corrupt a comparison

1. **`model_results` has one entry per revision, and stub revisions carry zero task
   results.** `intfloat/e5-small-v2` appears twice: a real revision with 131 task
   results and an `external` stub with 0. A naive
   `{mr.model_name: len(mr.task_results)}` keeps whichever came last and reports a
   fully-evaluated model as having no results. Always pick the best-covered revision.
2. **MTEB aggregates partial coverage without complaining** — it logs "Some task
   results are missing. Filling results with None" and returns a mean anyway. A mean
   over a subset of tasks is *not* comparable to a mean over all of them. Always check
   `n_tasks == len(benchmark.tasks)` before putting two models on the same axis.

3. **`n_active_parameters == 0` is a real value, not a missing one.** 34 models report
   zero active parameters: static embedding models (potion, model2vec,
   static-similarity-mrl) put *every* parameter in the lookup table, so
   `n_parameters - n_embedding_parameters` is genuinely 0 and nothing is computed per
   token. Only `None` means unknown. Treating falsy as missing silently deletes the most
   interesting end of any size comparison — and `log(0)` means a log axis needs an
   explicit break to show them, not a fudged "0.1M".

### Never run two fetches at once

`load_results()` updates the shared cache at `~/.cache/mteb/remote` with
`git reset --hard origin/main`. Two processes doing that against the same repo collide,
and the loser dies with `CalledProcessError ... exit status 128`. Run fetch scripts
**sequentially**, even across different post folders — the wall-clock saving is not worth
a half-finished card.

### Whole-registry loads, and what they cost

- `MTEB(eng, v2)` has **41 tasks** against Multilingual v2's 131. Scoring all ~834
  registered models takes **~15 minutes** on eng v2; the same over 131 tasks does not
  finish in any reasonable time. Any post about the field as a whole should use eng v2.
- **`load_results` drops partially-evaluated models from `model_results`, and
  `get_score` gives them `Mean(Task) = None`** — but they *do* remain as keys in the
  `get_score` result. So a "how many models have any results" count must come from the
  keys of `agg`, not from `model_results` and not from rows with a non-null score. Both
  of the latter silently report "any results" as identical to "complete results".
- On eng v2: ~400 models have some results, **99 have all 41 tasks**.

### Coverage is sparse at the small end

Of 120 text models with ≤60M active parameters, only 9 have any results on
`MTEB(Multilingual, v2)`, and fewer still have complete coverage. Peer comparison for
small models is therefore thin — expect a handful of points, not a cloud. This is the
concrete answer to whether new results are usable without additional analysis: the
numbers are trustworthy, but the *comparison set* needs building and checking.
