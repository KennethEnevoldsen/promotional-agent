# Working with the MTEB API

Facts that cost time to discover and are not recoverable by reading the code.

## The parts that surprise

- **The results repo is cached at `~/.cache/mteb/remote`** (~3.1 GB, 659 model dirs).
  `mteb.load_results()` pulls the latest into it.
- **Budget ~3 minutes before anything happens.** `import mteb` measured **190 s** on this
  machine — it pulls torch, transformers and the whole task registry. Everything else is
  cheap by comparison: `get_benchmark` ~1.6 s, `get_model_metas()` effectively free,
  `load_results` roughly **4.5 s per model** regardless of how many tasks the benchmark
  has.

  So the cost model is `190 + 4.5 x models` seconds, near enough. A 6-model cohort is
  ~3.5 min, 152 models is ~15 min, the whole registry is an hour plus. **Task count
  barely matters** — an 8-task benchmark over 152 models is no cheaper than a 41-task one
  over the same models.

  Two consequences: always pass a `models=` filter, and never assume a small benchmark
  means a fast load. Pick the cohort first from the filesystem or
  `mteb.get_model_metas()`, both of which are instant.

- **Run long loads unbuffered.** Python buffers stdout through a pipe, so a script killed
  by a timeout prints *nothing* — not even the progress it had made. Use `python -u` or
  `flush=True`; otherwise a 10-minute failure tells you nothing about where it went.
- **Aggregate with `Benchmark.get_score(results)`**, never by averaging task scores by
  hand. It is the same path the leaderboard uses and returns `{"Mean(Task)": …,
  "Mean(TaskType)": …}` per model.
- **"Active parameters" has two meanings; know which one you are using.** MTEB's
  `n_active_parameters` is `n_parameters - n_embedding_parameters` — the encoder,
  excluding the vocabulary table. Bekko's paper uses the same definition and says so
  explicitly, noting it "differs from the 'active parameters' of the Mixture-of-Experts
  literature", where the term means the experts actually routed to.

  Both are reaching for the same idea — count the parameters that cost compute — and
  differ only in which non-computing parameters they drop: unrouted experts, or a table
  lookup that is a memory access rather than a FLOP. The two agree for ordinary models
  (`Qwen3-Embedding-8B`: 6.95B of 7.57B) and diverge sharply when the vocabulary
  dominates (`bekko-a8m`: 7.7M of 106M; a static model: 0 of 108M).

  The consequence for writing: a static model having **0** active parameters is correct
  and meaningful under MTEB's definition — it runs no arithmetic at all. Under the MoE
  reading it would be nonsense. Say which you mean when the distinction could bite.

  Note also that `a8m` / `a25m` borrows MoE naming (compare `Qwen3-30B-A3B`), so these
  models look like MoEs at a glance. They are not — check `modelType` and
  `n_active_parameters_override` before describing any architecture.

  Bekko is a **layer-pruned mmBERT-small**: the paper prunes 22 layers to 4 (`a8m`) or
  13 (`a25m`), taking non-embedding parameters from 42M to 7.7M / 24.9M while the 98M
  vocabulary matrix is untouched. Metadata alone cannot tell you that — `n_parameters`
  and `n_embedding_parameters` are consistent with several architectures. **Read the
  paper before describing how a model is built**; three rounds of checking parameter
  counts here still produced the wrong description, because the numbers were never the
  thing in question.

- **Do not write "per token".** Active parameters are a fixed count for a dense model —
  the same weights run for every token. "Computes 7.7M per token" implies a quantity that
  varies, which is true only for mixture-of-experts routing. Say "7.7M active
  parameters", or "of which 7.7M are active".

  Two different things produce `active < total`, and they are opposites: a large
  **embedding table** (Bekko — 98M of 106M is vocabulary lookup) or **expert routing**
  (MoE, where `n_active_parameters_override` is set). Check `n_embedding_parameters` and
  the override before describing the mechanism. Neither Bekko nor
  `static-similarity-mrl` is MoE; both have `override = None`.

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
- On eng v2: ~400 models have some results, **99 have all 41 tasks**. On
  `MTEB(Law, v1)`: **152 models have all 8 tasks**, five of them legal-domain
  specialists.

- **Find a cohort from the filesystem when you only need coverage, not scores.** Walking
  `~/.cache/mteb/remote/results/<model>/<revision>/<Task>.json` and intersecting with the
  benchmark's task names takes seconds and needs no import. That is how to answer "who
  has complete results here" before paying the 190 s.

### Coverage is sparse at the small end

Of 120 text models with ≤60M active parameters, only 9 have any results on
`MTEB(Multilingual, v2)`, and fewer still have complete coverage. Peer comparison for
small models is therefore thin — expect a handful of points, not a cloud. This is the
concrete answer to whether new results are usable without additional analysis: the
numbers are trustworthy, but the *comparison set* needs building and checking.
