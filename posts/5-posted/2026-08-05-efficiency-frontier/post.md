---
id: 2026-08-05-efficiency-frontier
type: state_of_field
trigger_date: 2026-08-01
trigger: standing survey of the registry (no single event)
approved_by: kennethenevoldsen (explicit instruction, 2026-08-02)
scheduled_for: 2026-08-05T09:00:00+02:00
expires: 2026-11-01
sources:
  - https://leaderboard.mteb.org
verified: true
evidence: data.json
media: card.png
posted_on: 2026-08-05
url: https://bsky.app/profile/mteb.org/post/3msdaguqewd2d
---

```
The best embedding score available at the end of 2023 needed a 304M-parameter model.

Today the same score comes from an 11M one — 28x fewer active parameters.
```

## Why this post

This is the Bekko post's argument at field scale. That post showed one small model
sitting on the frontier; this one shows the frontier itself moving left over three
years. It is the more durable version of the story, because it does not depend on any
single submission being impressive.

## The claim

Pareto frontiers of score against **active** parameters on MTEB(eng, v2), for models
released by end-2023, by end-2024, and today. Each frontier is the set of models nothing
smaller beats.

| | best score | at | 
|---|---:|---:|
| by end-2023 | 62.32 | 303.9M active (`sdadas/mmlw-e5-large`) |
| today, same score | 63.97 | 11.0M active (`MongoDB/mdbr-leaf-mt`) |

**27.6x fewer active parameters** for a score that is slightly better, not merely equal.
The card rounds this to 28×; `data.json` carries the exact figure.

Peak score also rose — 62.32 to 75.98 — but that is the less interesting half. Peak
scores rising is expected; the cost of a *given* quality collapsing by more than an order
of magnitude is the part that changes what people can deploy.

## Static models are on the frontier

`minishlab/potion-base-32M` scores **54.63 with no active parameters at all** — a pure
lookup table. It sits on the current frontier and above two models that would otherwise
appear there.

This nearly got lost. The first pass filtered with `if active:`, which treats a genuine
zero as a missing value and silently deleted every static model — the same bug that had
to be fixed once already in the Bekko post. Zero active parameters is a real measurement.
It gets its own band on the axis, behind an explicit break, because `log(0)` has no
position and nudging them to "0.1M" would erase the one number that makes them
interesting.

## What this post must not claim

**Not "models got 28× more efficient".** The comparison is between two different models
from different labs with different training data. It says what the field now offers at a
given size, not that anyone shrank anything.

**Not a picture of 2023 as it looked in 2023.** These are release dates, not evaluation
dates: a model released in 2023 may have been submitted to MTEB much later, so each
frontier is *what existed by that date, as known today*. Only 20 models with complete
results were released by end-2023, so that frontier is sparse and probably sits below
where the true 2023 state of the art would have been. Both caveats are in `fetch.py` and
`data.json`; the card carries the second in its footer.

**Not a claim about total size.** The axis is active parameters — MTEB's
`n_active_parameters`, meaning the encoder excluding the vocabulary table.
`mdbr-leaf-mt` has more total weights than 11M.

Worth knowing that this is not the mixture-of-experts sense of the term; Bekko's paper
uses the same definition as MTEB and notes the difference explicitly. None of the models
plotted here are MoE. It matters most at the left of the axis, where a static model sits
at 0 — correct under this definition, nonsense under the other.
