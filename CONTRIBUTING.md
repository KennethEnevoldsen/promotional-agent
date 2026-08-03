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

### Default to MTEB(Multilingual, v2)

Unless the post is specifically about English, or about a domain or modality that has its
own benchmark, **`MTEB(Multilingual, v2)` is the general-purpose benchmark**. It is newer,
less exposed to overfitting than the English set, and it describes performance for far
more people. `MTEB(eng, v2)` answers a narrower question and should be chosen on purpose,
not by default.

This is worth stating because the default slipped once already. Two state-of-the-field
posts were built on `eng v2` for a purely mechanical reason — 41 tasks loaded faster than
131 — which stopped being true once load cost turned out to scale with model count rather
than task count, and stopped mattering entirely once the leaderboard API made either
about a second. A performance workaround outlived its cause and quietly narrowed the
claims to English.

If you use `eng v2`, say in the post why English is the right scope for that claim.

### Curate for breadth

This account exists to encourage embedding models that work broadly — across languages,
domains and modalities. What it chooses to cover is itself a signal about what counts as
progress, so the *mix* of posts is an editorial object, not just the individual posts.

Check the mix at scheduling, over roughly the last ten posts:

- **Languages.** English-only results are a narrow slice. If several posts running have
  been English, prefer a multilingual or non-English one.
- **Modalities.** Text dominates by volume. Audio, image and video work is
  under-represented relative to how much of it is landing — the MOEB cluster added 18
  audio and video tasks in a month and none of it has been posted.
- **Domains.** Legal, code, medical and finance benchmarks exist and get far less
  attention than the general leaderboards.
- **Kinds of post.** Model announcements are the easiest to produce and will crowd out
  dataset, benchmark and feature posts if nothing pushes back.

When two candidates are otherwise close, **prefer the one that broadens coverage**. When
a whole area has gone quiet in the feed but not in the repos, that is a reason to go
looking rather than to wait.

This is a bias correction, not a quota. A genuinely important English text model should
still be posted; the rule is to notice when a run of posts has narrowed, and to reach for
breadth when the choice is otherwise a toss-up.

### Ask who is missing before believing a ranking

A leaderboard rank is a fact about **who submitted**, not about who is best. On the big
general benchmarks the two are close enough to ignore. On a domain benchmark they are
not: a domain model has every incentive to submit domain results, and a frontier
generalist has none.

This is measurable, so measure it. Take the top ~20 models on a broad benchmark and check
how many appear in the cohort you are about to rank. For `MTEB(Law, v1)`: **14 of the top
20 `MTEB(eng, v2)` models had no complete Law results**, including the top four overall.
A post concluding "specialists beat generalists" from that ranking would have been
measuring submission behaviour and calling it capability.

Two ways out, in order of preference:

1. **Find the claim that survives.** A *within-model* comparison — the same model on two
   benchmarks — is untouched by who else submitted. `Jasper-Token-Compression-600M` is
   5th on English and 29th on legal; that holds no matter who is absent, and it turned
   out to be the more interesting finding anyway.
2. **Scope the claim to the cohort.** "Of models evaluated on X" is honest and often
   enough. Say it in the post, not only in the notes.

Never state or imply the unscoped version. The absent models are usually absent precisely
because they are the ones that would test the claim.

### One post, one claim

A model announcement and a claim about the field are different posts even when they use
the same query and the same chart. `dinghy-law-family` says "this model is first";
`legal-specialisation` says "specialists beat generalists here". Same eight rows, but the
subject differs and so does the risk: an announcement is wrong only if a number is wrong,
while a field claim is wrong if a *category* is wrong.

The tell is in the card. An early dinghy-law card coloured every legal-domain model,
which encoded the field claim on a post that was announcing a model — and left a reader
asking what the colour meant, because nothing on the card was making that argument.

**Colour may only encode the claim the post is actually making.** If a distinction is
worth colouring, it is worth a sentence; if it does not get a sentence, it should be
context grey.

When two posts do overlap, mark it (`competes_with:` in the frontmatter) and choose
between them rather than running both in a week. Merging is sometimes the better answer,
but a merged post is a third thing that needs its own draft, not either original with a
paragraph bolted on.

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

**Voice is "we", meaning the MTEB team** — the org is accountable for what goes out
whoever drafted it. Never first-person-singular: the tooling is not a character, and a
character invites the replies this account does not make. "We" is for accountability, not
warmth. `profile.md` has the account-level identity.

**Anything true of every post belongs in the bio, not the feed.** If a draft is mostly
explaining what the account is, it is competing with `profile.md` and will lose.

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

### The LinkedIn version

**Default: the LinkedIn post is the Bluesky text.** Same words, no second version.

Write a separate one only when the 300-character limit forced out something a reader
genuinely needs — usually a caveat that prevents a misreading. Then say, above the block,
what that something is. If you cannot name it in a sentence, there was no reason.

When it exists it goes in `post.md` under a `## LinkedIn` heading inside a
```` ```linkedin ```` block — same file, and the fence keeps it out of the 300-character
check, which only scans bare ``` blocks.

**Same voice, not a second one.** The failure mode is two formats drifting into two
personalities — one terse and factual, the other doing thought leadership. More room is
not a reason to become a different account.

The extra length is for a caveat, a coverage limit, or the scope a card stopped
printing. It is **not** for restating the same sentence at greater length, adding a
call-to-action, or reaching for a broader claim to justify the word count. A LinkedIn
version that needs a bigger claim to earn its length does not need the length.

Keep it close to the Bluesky text and derive both from the same `data.json`. If the two
ever disagree on a number, that is a bug rather than a style difference.

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

**This move is the human's, and only the human's.** `3-review` means "a person has not
looked yet". An agent that drafts a post and then schedules it has removed the only step
that makes any of the rest trustworthy — and it is an easy mistake, because the work
feels finished. Record who decided in `approved_by:`; `mteb-validate` refuses a scheduled
post without a named approver.

**Add the date to the folder name when you move it here** — `dinghy-law-family` becomes
`2026-08-06-dinghy-law-family` — and set `scheduled_for:` to match. That is the only
point in the pipeline where a folder gets a date, which is what keeps the date
meaningful.

---

## Validate before moving a post forward

```bash
uv run mteb-validate                    # whole pipeline
uv run mteb-validate --stage 3-review   # one stage
```

It checks what a machine can: the 300-character limit, required frontmatter per stage,
that `media:` points at a file that exists, that a thread declares as many
posts as it contains, that every card carries alt text and has been rendered, that folder dates
appear only once scheduled and match `scheduled_for:`, and that no two posts share a day.

**A clean run means nothing is obviously broken. It does not mean the post is good.**
Whether a cohort is fair, whether a claim is scoped to its evidence, whether the subject
is worth anyone's attention — none of that is checkable, and all of it is in this file.
Treat the validator as the floor, never the bar.

## Rejecting

Every rejection needs a `reason:`. `rejected/` is the most auditable thing in the repo —
it is the record of what the pipeline chose *not* to say, and the first place to look if
the account's judgement is ever questioned.

Rejections stick: `mteb-scan` skips any PR already referenced anywhere in the pipeline,
so a rejected candidate does not reappear the next morning. If circumstances change
(results finally land), move the folder back to `1-candidates/` by hand.
