# Working on posts

How a candidate becomes a scheduled post, and the editorial rules that decide what gets
said. `README.md` has the pipeline shape; `AGENTS.md` has the rules in one-line form.
This file is the reasoning behind them, which is what you need while actually drafting.

Written as instructions because that is what an agent needs, and read as documentation
because that is what a person auditing it needs. Same text either way.

---

## 1 → 2: is this worth working up?

A candidate is a PR and a guess. Most die here, and that is the point — the repos merge
3-4 PRs a day, so the bottleneck is not finding things to post but choosing the one or
two a week worth saying.

**A model addition is postable only once results are merged.** A `ModelMeta`
registration with no scores is plumbing, not news. The pairing — a PR in `mteb` plus its
partner in `results` — is the single most reliable trigger there is.

If the results are not there yet, that is `blocked_on:`, not a rejection. If they are
never coming (metadata-only, a revision bump, a wrapper fix), reject it with that as the
reason.

**Do not trust labels.** Roughly half of genuine model additions carry no label at all,
and `jina-reranker-v3.5` carried `new model` while being pure plumbing. Title
conventions (`model:`, `task:`, `[MOEB]`, `fix:`, `ci:`) are far more consistent, which
is what `mteb-scan` keys off.

**Patch releases are not features.** The package shipped 8 releases in 12 days. Only
minor/major versions, or a specifically notable capability, qualify.

**Two categories are almost never worth a post:**

- *Minor corrections and bug fixes.* The exception is a fix with a result a reader would
  find surprising — a large speed-up, say — where the number is the story.
- *Plumbing for a larger research project.* Scaffolding for work that has not landed yet
  has nothing to announce. This one is contextual: if the project itself is the news and
  it is public, that is a different post.

**Results added for an existing model** are a real category and easy to miss, since the
model itself was announced long ago. Worth a post only when the new numbers change
something — a new benchmark, a size class nobody had covered, a surprising result.

**Clusters can be grouped or spread.** 18 audio/video tasks landed in one month. Group
them into one roundup when no individual item carries its own story; spread them across
days when they do.

---

## 2 → 3: making it checkable

This is the stage that earns the account its credibility. Everything a reader could
verify must be verified before the post reaches review.

### Recompute every number

Contributor-supplied score tables are *claims*. MTEB's account restating them verbatim
lends the benchmark's credibility to numbers nobody checked. Pull them from the results
repo through `Benchmark.get_score()` — the same aggregation the leaderboard uses — and
compare. If recomputation disagrees with the PR, the post does not run.

`docs/mteb-data.md` covers the API and the several ways this goes silently wrong.

### Choose the cohort, and record it

Any comparison names *other people's models*, so the cohort has to be one those authors
would accept. This is the one editorial judgement a reader cannot check against the
leaderboard, which is why it lives in `fetch.py` as code rather than in prose.

Two filters that turned out to matter more than they look:

- **Peers must be built for the benchmark being cited.** Bekko's first cohort swept in
  `e5-small-v2`, `bge-small-en-v1.5` and `all-MiniLM-L6-v2` — English-only models
  scoring 41-45 on a *multilingual* benchmark. They score low because they were never
  built for it. Keeping them would have inflated Bekko's margin **and** implied three
  well-regarded models were worse than they are.
- **Complete task coverage only.** MTEB aggregates partial results without complaining.
  A mean over a subset of tasks is not comparable to a mean over all of them.

The general form: a comparison flattered by models that were never in the race is the
fastest way for this account to lose the trust it exists to protect.

`data.json` records every model that qualified, including any that beat the subject.
Filtering it to the flattering rows would make it useless as evidence.

### Write the post

**300 characters.** This is the dominant constraint. LMArena's LinkedIn page is the
tonal reference, but it transfers as tone and cadence only — those posts run 5-10x too
long structurally.

House style: factual, specific, understated. Lead with the concrete thing. No hype
adjectives, no emoji strings, no hashtag stuffing.

**Name models by their full Hugging Face id** — `hotchpotch/bekko-embedding-v1-a8m`, not
`bekko`. It costs characters, but an abbreviation is harder to check against the
leaderboard and two models can abbreviate to the same string.

Post shapes that have worked:

| type | shape |
|---|---|
| `model_addition` | what it is · the number that makes it interesting · the benchmark it is on |
| `dataset_roundup` | a cluster's shared theme, then the task names with a one-word gloss each |
| `benchmark_addition` | what it measures and why it did not exist before |
| `state_of_field` | a claim about the whole registry, with the cohort stated |
| `feature_release` | minor/major versions only; the one thing that matters to users |

**A card buys back character budget.** Once a draft carries two model names, two scores,
a benchmark name and a credit line it is already at ~290 characters with nothing left to
say why anyone should care. Moving the numbers into the image frees the text to make the
argument. See `docs/card-design.md`.

### Credit

Every post names the people whose work it describes. This is a community project and the
posts should read like it.

Credit and tagging are separate. Credit is unconditional and uses the GitHub handle as
plain text. Tagging requires an opt-in handle in `social-handles.yaml` — never infer one
from a name or profile. A wrong-person mention is precisely the spammy, follower-farming
behaviour this account exists to avoid.

State-of-the-field posts describe no single person's submission and carry no credit line.
That is a deliberate signal, not an oversight.

---

## 3 → 4: scheduling

Floor is one post a week, ceiling is **one a day**. With 3-4 PRs merging daily the
ceiling binds, not the floor — the job is spreading material evenly, not hunting for it.

Never post twice in a day to clear a backlog. A long queue means spread wider, not batch.
A thin week is not a reason to promote something that failed the rules above; that is
what the roundup shape exists for.

Check `expires:` before scheduling. News older than about a month is not news, and a
post that sat in review past its window should be rejected rather than shipped stale.

**Add the date to the folder name when you move it here** — `dinghy-law-family` becomes
`2026-08-06-dinghy-law-family` — and set `scheduled_for:` to match. That is the only
point in the pipeline where a folder gets a date, which is what keeps the date
meaningful.

---

## Rejecting

Every rejection needs a `reason:`. `rejected/` is the most auditable thing in the repo —
it is the record of what the pipeline chose *not* to say, and the first place to look if
the account's judgement is ever questioned.

Rejections stick: `mteb-scan` skips any PR already referenced anywhere in the pipeline,
so a rejected candidate does not reappear the next morning. If circumstances change
(results finally land), move the folder back to `1-candidates/` by hand.
