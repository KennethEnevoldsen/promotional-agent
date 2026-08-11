---
id: 2026-08-10-openness
type: state_of_field
trigger: standing survey of the registry (no single event)
trigger_date: 2026-08-01
approved_by: kennethenevoldsen (explicit instruction, 2026-08-03)
scheduled_for: 2026-08-10T14:30:00+02:00
expires: 2026-11-01
verified: true
evidence: data.json
media: card.png
sources:
  - https://leaderboard.mteb.org
  - mteb ModelMeta.openness (weights / licence / training code / training data)
---

```
Most embedding models publish their weights. Far fewer publish what it took to build them.

Of 172 models with complete MTEB(Multilingual, v2) results, about 1 in 16 are fully open — weights, training code and training data. 153 publish weights alone; 8 publish none of it.
```

## LinkedIn

The Bluesky text plus the exact counts, which fit here and do not fit in 300 characters.
Nothing else meets the rule for a separate version, which is why there is nothing else.

```linkedin
Most embedding models on MTEB publish their weights. Far fewer publish what it took to build them.

Of the 172 models with complete MTEB(Multilingual, v2) results: 153 are open-weight, 11 are fully open (weights, training code and training data), and 8 are proprietary.

Fully reproducible models are about one in sixteen of the board.
```

## The claim

Three tiers, from `ModelMeta.openness`:

| tier | rule | any results | complete |
|---|---|---:|---:|
| proprietary | no open weights | 51 | 8 |
| open weights | weights, but not both code and data | 365 | 153 |
| open source | weights + training code + training data | 56 | 11 |

**Fully reproducible models are 11 of 172** — about one in sixteen. "Open" in common usage
means the middle tier; the gap between publishing weights and publishing the recipe is
where almost the entire field sits.

**Why the post says "about one in sixteen" and not the percentage.** The first version said
"under 6%", which was true when it was written and false four days later: one more fully
open model merged and 10-of-171 (5.85%) became 11-of-172 (6.40%). A threshold claim is
brittle by construction — a single submission flips it, and the leaderboard is other
people's to change. A ratio says the same thing and survives the population moving, which
is the only sensible way to phrase a claim about a board that will not hold still. The
exact counts stay in the LinkedIn version and in this file, where they are dated evidence
rather than a live assertion.

The best model in each tier:

| tier | best | score |
|---|---|---:|
| open weights | `microsoft/harrier-oss-v1-27b` | **74.27** |
| proprietary | `Bytedance/Seed1.6-embedding-1215` | 70.26 |
| open source | `nvidia/llama-embed-nemotron-8b` | 69.46 |

## Why multilingual, and why that mattered

An earlier version of this post used `MTEB(eng, v2)`, chosen for a purely mechanical
reason — 41 tasks loaded faster than 131. That justification evaporated twice (load cost
scales with model count, not task count; then the API made either about a second), but
the choice stayed and quietly turned a claim about the field into a claim about English.

Redoing it on the multilingual set **changed the answer**. On English the best proprietary
and best open-weight models were separated by 0.01 points — effectively tied. On
multilingual the best open-weight model leads by **4 points**. Same question, different
benchmark, materially different picture. That is the argument for the default, made
concrete.

## What this post does not claim

**Not that open models are better than proprietary ones.** Only 8 proprietary models have
complete results out of 51 with any, and the well-known API models are largely absent —
they have partial coverage rather than none. A four-point lead over a thin, self-selected
sample is not evidence about capability. The composition claim is what the data supports.

**Not that one in sixteen is a scandal.** Publishing training data is genuinely hard: licensing,
scale, and competitive cost are all real. The number is worth stating precisely because
it is easy to assume "open model" means reproducible when it almost never does.

## Coverage, stated plainly

Requiring all 131 tasks drops the field from 472 rows to 172. The filter costs each tier
a similar share — proprietary 8 of 51, open-weight 153 of 365, open-source 11 of 56 — so
it is not biased against any one tier, but it is why the absolute numbers are small.
Partial results are excluded rather than averaged: a mean over a subset of tasks is not
comparable to a mean over all of them.

## Notes

Uses the leaderboard API rather than the `mteb` package: ~2 seconds against ~15 minutes,
scores validated against a local `Benchmark.get_score()` run, and better coverage —
results that fail the package's revision validation still appear here.

The three-tier split flattens a six-field record (weights, licence, training code,
training data, paper, model card). Which flattening to use is editorial: "could someone
else rebuild this" is the line MTEB cares about, and the one that disappears when people
say "open model".

No contributor credit — this describes the leaderboard in aggregate rather than anyone's
submission.
