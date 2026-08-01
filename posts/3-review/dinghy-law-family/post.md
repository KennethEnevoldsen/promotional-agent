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
On MTEB(Law, v1), the five best models are all built for law.

Hanno-Labs/dinghy-law-4b-v1 leads at 71.22, and the 0.6B version places 4th — ahead of every general-purpose model, including one 23x its size.
```

## The claim

Of **159 models with complete `MTEB(Law, v1)` results**, legal-domain models take the
first five places. The first general-purpose model is sixth.

| rank | score | size | model |
|---:|---:|---:|---|
| 1 | **71.22** | 4.0B | `Hanno-Labs/dinghy-law-4b-v1` |
| 2 | 70.37 | 7.6B | `Mira190/Euler-Legal-Embedding-V1` |
| 3 | 69.33 | 8.0B | `minetta/nemotron-3-embed-8b-legal` |
| 4 | **65.83** | 0.6B | `Hanno-Labs/dinghy-law-0.6b-v1` |
| 5 | 65.39 | undisclosed | `voyageai/voyage-law-2` |
| 6 | 64.66 | 14.0B | `codefuse-ai/F2LLM-v2-14B` — *first general-purpose* |

`dinghy-law-0.6b` at 0.6B parameters beats `F2LLM-v2-14B` at 14.0B — **23x smaller**, on
legal tasks, because it was built for them.

## Why this and not "a new model was added"

The trigger was `mteb#5058` registering `dinghy-law-8b-v1`. That model has **no results
PR** and is not yet in the registry, so on its own it is not postable — a registration
without scores is plumbing.

But the scanner's mis-pairing (it matched the 8b model to the 4b's results) sent me
looking at the family, and the family is the story: 0.6b on 2026-07-13, 4b on 2026-07-22,
8b on 2026-07-31, all from `trashhalo`. Two of the three have complete results and both
land in the top four.

A mis-paired candidate is not a dead one. The pairing check exists to find the real
subject, not only to reject.

## Sources and verification

This post uses the **leaderboard API** rather than the `mteb` package —
`mteb-leaderboard-backend.hf.space` — which returns in ~2 seconds against ~14 minutes
locally. Two reasons beyond speed:

- **It is more complete.** `voyageai/voyage-law-2` has all 8 Law task files on disk but
  its results sit under revisions `1` and `no_revision_available` and do not survive
  `load_results`' revision validation. The API includes it. A post claiming the top of
  the legal leaderboard is domain models, while silently omitting the best-known legal
  model, would be flattery by omission — and as it happens `voyage-law-2` places 5th,
  inside the claim rather than against it.
- **The scores are validated.** Eight models across `MTEB(Law, v1)` and
  `MTEB(Multilingual, v2)` were checked against a local `Benchmark.get_score()` run and
  match exactly.

**Sizes are total parameters, not active.** The API's `activeParamsB` currently returns
total — it does not subtract the embedding table (see `issue.md`, filed upstream). Total
is also the right axis for this claim, which is about model size rather than per-token
inference cost. Do not switch this post to active parameters without re-checking that
field.

## What a reader cannot check

**The legal-domain list is hand-maintained.** There is no metadata flag for "trained for
law", so membership is an editorial judgement: `dinghy-law` (both), `Euler-Legal`,
`nemotron-3-embed-8b-legal`, `voyage-law-2`. It lives in `fetch.py` rather than in prose
so that it is inspectable and a wrong entry shows up in a diff.

The risk is a false negative — a domain model not on the list would appear as
general-purpose and could sit above the break, quietly weakening the claim. The five were
found by name matching on "law"/"legal", which would miss a legal model named for
something else.

## Notes

Credit: `trashhalo` submitted all three models and both results PRs. Not tagged — no
Bluesky handle in `social-handles.yaml`.

Two proprietary models (`voyage-law-2`, `voyage-3`) do not publish parameter counts. The
card says "size undisclosed" rather than dropping them or printing a zero; an undisclosed
number is not a small one.

**When the 8b results land this post gets better, not stale** — a three-point size sweep
within one family, on a domain benchmark, is a stronger version of the same claim. That
is an argument for holding it rather than posting the moment the material is sufficient.
