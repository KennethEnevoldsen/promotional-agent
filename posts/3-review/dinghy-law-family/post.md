---
id: dinghy-law-family
type: model_addition
trigger: mteb#5058 (8b registration) — postable content is results#631 + results#613
trigger_date: 2026-07-31
expires: 2026-08-31
subject: Hanno-Labs/dinghy-law-4b-v1
verified: true
evidence: data.json
media: card.png
alt: card.txt
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5058
  - https://github.com/embeddings-benchmark/results/pull/631
  - https://github.com/embeddings-benchmark/results/pull/613
---

```
New on MTEB: Hanno-Labs/dinghy-law-4b-v1, a legal-domain embedding model, takes 1st on MTEB(Law, v1) at 71.22.

Its 0.6B sibling places 4th at 65.83 — the smallest model in the top eight by an order of magnitude.
```

## The claim

`dinghy-law-4b-v1` is first of **159 models with complete `MTEB(Law, v1)` results**, at
71.22. `dinghy-law-0.6b-v1` is fourth at 65.83, and at 0.6B is roughly a tenth the size
of everything else near the top.

| rank | score | size | model |
|---:|---:|---:|---|
| **1** | **71.22** | 4.0B | `Hanno-Labs/dinghy-law-4b-v1` |
| 2 | 70.37 | 7.6B | `Mira190/Euler-Legal-Embedding-V1` |
| 3 | 69.33 | 8.0B | `minetta/nemotron-3-embed-8b-legal` |
| **4** | **65.83** | 0.6B | `Hanno-Labs/dinghy-law-0.6b-v1` |
| 5 | 65.39 | proprietary | `voyageai/voyage-law-2` |

## Scope of the claim

The rank is "first of 159 models with complete results", and that qualifier is doing real
work: 14 of the top 20 models on `MTEB(eng, v2)` have never run `MTEB(Law, v1)`. Being
first here means first among those who entered, which is the only thing any leaderboard
rank ever means, but it is worth stating plainly on a domain benchmark where entry is so
clearly self-selecting. The card says "top 8 of 159 models with complete results" for
exactly that reason.


This is a **model announcement**, not a claim about specialisation as a phenomenon. The
same data shows legal-domain models holding the top five places, which is a genuinely
interesting finding — but it is a different post with a different subject, and it is
drafted separately as `2-drafting/legal-specialisation`. The two overlap and may compete
for a slot; decide between them rather than running both in the same week.

That distinction drove the card design. An earlier version coloured every legal-domain
model, which encoded the *other* post's claim and left a reader wondering what the purple
meant. Here the subject models are in accent and everything else is context grey, which
is what a model announcement should say.

## Why this rather than the 8b addition

The trigger was `mteb#5058` registering `dinghy-law-8b-v1`, which has **no results PR**
and is not yet in the registry. A registration without scores is plumbing, not news.

The scanner mis-paired it (matching the 8b model to the 4b's results), and chasing that
error is what surfaced the family: 0.6b on 2026-07-13, 4b on 2026-07-22, 8b on
2026-07-31, all from `trashhalo`. A mis-paired candidate is not a dead one — the pairing
check exists to find the real subject, not only to reject.

## Sources and verification

Uses the **leaderboard API** (`mteb-leaderboard-backend.hf.space`), ~2 seconds against
~14 minutes for the equivalent local computation. Two reasons beyond speed:

- **More complete.** `voyageai/voyage-law-2` has all 8 Law task files on disk but its
  results sit under revisions `1` and `no_revision_available` and do not survive
  `load_results`' revision validation. The API includes it, at 65.39 — fifth, just below
  `dinghy-law-0.6b`. Omitting the best-known legal model from a legal ranking would have
  been flattery by omission.
- **Validated.** Eight models across `MTEB(Law, v1)` and `MTEB(Multilingual, v2)` were
  checked against a local `Benchmark.get_score()` run and match exactly.

**Sizes are total parameters, not active.** The API's `activeParamsB` currently returns
total — it does not subtract the embedding table (`issue.md`, filed upstream). Total is
the right axis here anyway, since the claim is about model size rather than per-token
cost. Do not switch to active without re-checking that field.

Shown to two significant figures. `4.028B` is false precision on a card when the
comparison being made is order-of-magnitude.

## Notes

Domain membership is decided by the model name declaring a legal domain, which is the
strongest signal available: of the five legal models in the top five, none declares a
legal training dataset in its metadata, and three list no training data at all. For this
post it is a supporting detail — the claim is a rank, not a category — but the same check
matters much more to `legal-specialisation`, where the category *is* the claim.

Credit: `trashhalo` submitted all three models and both results PRs. Not tagged — no
Bluesky handle in `social-handles.yaml`.

Two proprietary models say "proprietary" rather than reporting a size. An undisclosed
number is not a small one, and a blank invites the reader to assume.

**When the 8b results land this post gets better, not stale** — a three-point size sweep
within one family on a domain benchmark is a stronger version of the same claim. That is
an argument for holding rather than posting the moment the material is sufficient.
