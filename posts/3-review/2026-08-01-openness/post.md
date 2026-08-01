---
id: 2026-08-01-openness
type: state_of_field
trigger_date: 2026-08-01
trigger: standing survey of the registry (no single event)
expires: 2026-11-01
sources:
  - https://leaderboard.mteb.org
  - mteb ModelMeta.openness (weights / licence / training code / training data)
verified: true
evidence: data.json
media: card.png
alt: card.txt
---

```
Most embedding models on MTEB publish their weights. Far fewer publish what it took to build them.

Of 98 models with complete MTEB(eng, v2) results: 75 open-weight, 14 fully open (weights + training code + data), 9 proprietary.

The top of each group is within ~1 point.
```

## The claim

Three tiers, from `ModelMeta.openness`:

| tier | rule | registered | any results | complete |
|---|---|---:|---:|---:|
| proprietary | no open weights | 57 | 41 | 9 |
| open weights | weights, but not both code and data | 628 | 302 | 75 |
| open source | weights + training code + training data | 149 | 49 | 14 |

The interesting number is the registry column against the last one, and the fact that
"open source" — meaning someone else could rebuild the model — is **18% of the registry
and 14 of the 98 models with complete results**. "Open" in common usage means the tier
above; the gap between publishing weights and publishing the recipe is where most of the
field sits.

## What this post must not claim

**Not a proprietary-vs-open frontier gap.** That was the first framing and the data does
not support it. Only 9 proprietary models have complete results, and the set is missing
OpenAI and Cohere entirely — both are registered, both have partial results in the repo,
neither completes all 41 tasks. "Best proprietary model" therefore rests on a handful of
submissions, and the current top of that lane is a single model from a lab nobody would
name as a frontier player.

So the post reports composition, which the data does support, and shows the counts on the
card so the thin lane is visible rather than asserted around.

**Not "open has caught up".** The top three scores are close (within about a point), but
with n=9 on one side that is a fact about who submitted, not about who is better. The
draft says the tops are close and stops there.

## Coverage, stated plainly

Requiring all 41 tasks drops the field from **392 models with some results to 98**. The
filter costs each tier a similar share — 22% of proprietary models with any results
survive it, 25% of open-weight, 29% of open-source — so it is not biased against
proprietary models specifically. But it is why the absolute numbers are small, and it is
why partial results are excluded rather than averaged: a mean over a subset of tasks is
not comparable to a mean over all of them.

Getting that funnel right took two attempts. `load_results` drops partially-evaluated
models from `model_results`, and `get_score` gives them a null `Mean(Task)` — so
counting "any results" from either source reports it as *identical* to "complete
results", which would have made the coverage caveat invisible in the very post that
depends on it. The count has to come from the keys of the `get_score` result.

## Notes

Benchmark is MTEB(eng, v2) rather than the multilingual one for a practical reason: 41
tasks instead of 131 is the difference between a whole-registry load that finishes and
one that does not. It also has the broadest model coverage, which is what matters when
the question is who is on the board at all.

The three-tier split flattens a six-field record (weights, licence, training code,
training data, paper, model card). The choice of *which* flattening is editorial:
"reproducible end to end" is the line MTEB cares about, and it is the one that
disappears when people say "open model".

**Open:** no contributor to credit here — this is the leaderboard in aggregate rather
than anyone's submission. Worth deciding whether state-of-the-field posts carry a
credit line at all, or whether the absence of one is itself the signal that no single
person's work is being described.
