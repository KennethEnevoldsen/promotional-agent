---
id: 2026-10-15-leaderboard-pareto-tag
type: feature_release
trigger: leaderboard-frontend#40 (Add Pareto identifier to models), merged 2026-10-05, closes mteb#5408
trigger_date: 2026-10-05
approved_by: kennethenevoldsen (explicit instruction, 2026-10-12)
scheduled_for: 2026-10-15T14:30:00+02:00
expires: 2026-11-02
verified: true
evidence: data.json
media: card-1-pareto-tag.png
thread: 2
sources:
  - https://github.com/embeddings-benchmark/leaderboard-frontend/pull/40
  - https://github.com/embeddings-benchmark/mteb/issues/5408
  - https://leaderboard.mteb.org
---

```
1/ The best embedding model you can afford to run can sit well down the MTEB leaderboard, because the ranking ignores size.

A new Pareto tag now marks it: no model with the same or fewer active parameters has a higher average score. Hover it to see the size range it leads.
```

```
2/ The tag follows the sidebar filters: limit the table to open weights, zero-shot models or one model type and it marks the best model at each size within that set. Models that publish no size can't be placed, so are never tagged.

Try it at leaderboard.mteb.org

Work by ayush1298.
```

## LinkedIn

The Bluesky thread as one post, word for word. The only difference is the credit line,
which tags Ayush on LinkedIn (`linkedin:` in `social-handles.yaml`; pick him from
LinkedIn's mention dropdown when pasting).

```linkedin
The best embedding model you can afford to run can sit well down the MTEB leaderboard, because the ranking ignores size.

A new Pareto tag now marks it: no model with the same or fewer active parameters has a higher average score. Hover it to see the size range it leads.

The tag follows the sidebar filters: limit the table to open weights, zero-shot models or one model type and it marks the best model at each size within that set. Models that publish no size can't be placed, so are never tagged.

Try it at leaderboard.mteb.org

Work by @Ayush Munot.
```

## The claim

The post text has no numbers. The card's scores are recomputed in `fetch.py` (see
`data.json`). Every statement in the text is about behaviour, checked against the frontend source on `main` (`fbb28ce`, which includes
the #40 merge commit `5d0f9a1`) and against the live site's JS bundle.

| post says | where it is true |
|---|---|
| "the ranking ignores size" | rank is Borda over tasks; size plays no part (`filters.svelte.ts`) |
| "no model with the same or fewer active parameters has a higher average score" | `paretoFrontier()` in `src/lib/pareto.ts`: x = active params, y = Mean (Task); ties on both axes keep every tied row |
| "Pareto tag" | `ModelCellName.svelte` renders a `Pareto` pill after the model name in the summary table |
| "Hover it to see the size range it leads" | `ModelHoverPortal.svelte` adds a "Pareto optimal" row reading `Best for 3.6 B–6.9 B active params` (from its own size up to the next frontier model's), `Yes`, `No` or `—` |
| "follows the sidebar filters" | frontier is recomputed over `candidates`, the rows that pass the sidebar filters (`filters.svelte.ts` ~l.841). The name search deliberately does *not* change it, same as rank |
| "open weights, zero-shot models or one model type" | real sidebar options: Openness → "Open weights", Zero-shot → "Only zero-shot", "Model type" facet |
| "publish no size can't be placed, so are never tagged" | `isParetoEligible()` requires both `activeParamsB` and `meanTask`; rows missing either are neither tagged nor able to dominate |

**Deployed:** the "Deploy to GitHub Pages" run for `fbb28ce` succeeded on 2026-10-10, and
the live bundle at leaderboard.mteb.org contains both `Pareto frontier (no model of equal
or smaller size scores higher)` and the `Best for … active params` string.

**Partial coverage cannot earn the tag.** Rows with incomplete task coverage have a null
Mean (Task) and are excluded, so a model cannot look Pareto-optimal on a subset of tasks.
That keeps the feature consistent with rule 6 without us having to say so.

## What must not be claimed

- **Not "the best model for its size" unqualified.** It is best on *average task score*
  among *models shown*, with size as *active* parameters. Hence "average score" and "same
  or fewer active parameters" in the text; "can sit well down" rather than "is often far
  down", which would be a frequency claim we have not measured.
- **Not that untagged models are worse.** A proprietary model with no published size is
  untagged because it cannot be placed. Part 2 says so; without that sentence a reader
  could take a missing tag on a well-known API model as a verdict.
- **Not that the tag and the rank agree.** The frontier uses Mean (Task); the table ranks
  by Borda. A tagged model can therefore sit *below* an untagged smaller one in the table.
  Samoed raised exactly this on the PR and the maintainers merged knowing it
  (KennethEnevoldsen: "not unproblematic", a more robust continuous score is future work).
  Not in the post: it is an edge case, and explaining Borda in 300 characters would bury
  the feature. If it draws confusion, the header tooltip on the live site already states
  the definition.
- **No claim about model types being comparable.** The size chart itself warns that active
  parameters don't capture late-interaction storage or cross-encoder scoring cost, and
  points users at the model-type filter, which is why part 2 names that filter.

## Why only this PR

Recently merged in `leaderboard-frontend` (backend changes live in the `mteb` repo):

| PR | merged | what | in this post? |
|---|---|---|---|
| #40 Pareto tag | 10-05 | tag, hover row, frontier line + "Pareto optimal" list on the Performance per Model Size tab, CSV column | **yes** |
| #4 + mteb#4900 Experiments | 10-01 | experiment variants (e.g. a multi-vector configuration) shown as their own rows; dot on models that don't cover all of a benchmark's modalities | no: its own story |
| #37 + mteb#5174 Custom grouping | 10-01 | benchmark-defined task groups as table columns (first used for LMEB "Memory Type") | no: its own story |
| #44 | 10-09 | openness selector visually highlighted | no: cosmetic |
| #45 | 10-10 | "availability" filter removed | no: removal, nothing to announce |
| #43 | 10-10 | duplicate info removed from model page | no: cleanup |
| #39, #36 | Aug | total params in hover; static models on size chart | no: older (August), small hover/chart additions |

There is no single story across these. A roundup of #40, #4 and #37 would need three
separate explanations in 300 characters each, which is the "reads like a diff" failure.
The Pareto tag is the one change any leaderboard user notices and can act on (pick a model
for a size budget), so it gets the post. #4 and #37 are each plausible posts on their own:
custom grouping pairs naturally with an LMEB follow-up, and experiment rows with a
late-interaction or multi-vector model post.

The one place they interact: the frontier is computed per row, so an experiment variant
from #4 can be tagged independently of its base model. Not worth a sentence here.

## Notes

**Why a thread.** Part 1 is the feature and what it means. Part 2 is what makes it a
tool rather than a badge (filters change the answer) plus the caveat that stops the
obvious misreading. Both earn their place; neither fits in the other's budget.

**Continuity with 2026-08-05-efficiency-frontier.** That post showed the size/score
frontier moving over time. This one is the leaderboard now drawing that frontier for
every reader. Deliberately not referenced in the text: a callback to our own earlier post
is about the account, not about the feature.

**Credit.** ayush1298 wrote the PR. KennethEnevoldsen, Samoed and isaac-chung shaped it in
review (colour, alignment with the over-time chart, the "Best for" range, which came from
Samoed asking why half of a top-10 was tagged); review is not credited in posts. ayush1298
has no entry in `social-handles.yaml`, so there is no @-mention.

**Not a version bump.** CONTRIBUTING restricts `feature_release` to minor/major versions
or "a specifically notable capability". The leaderboard frontend has no releases; this is
the second case. Requested by kennethenevoldsen on 2026-10-12.

**PR content handled as data.** The PR body and comments were read for what the feature
does, then checked against the source; nothing in them was treated as instruction.

## Decisions for the reviewer

1. **Card.** Text-only as drafted. The most informative image would be a real screenshot
   of the live table showing the tag and the hover row, which you can take yourself. It
   would show live leaderboard scores that this post has not recomputed (rule 1), so crop
   to the tag/hover or accept that the numbers are the leaderboard's own display. A
   schematic card was considered and not built: dots without data on a benchmark account
   read as data.
2. **Spacing.** `4-scheduled/2026-10-13-audio-video-input-config` is also a feature post; two in a row
   narrows the feed's mix. Suggest leaving a model or dataset post between them.
3. **"ranking ignores size".** Strictly true (Borda over task scores), but some readers
   will know the size filter exists. If you prefer, "the ranking doesn't account for size"
   is the same length and softer.
