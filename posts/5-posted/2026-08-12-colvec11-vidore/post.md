---
id: 2026-08-12-colvec11-vidore
type: model_addition
trigger: mteb#5010 (models) + results#643 (results, merged 2026-07-27)
trigger_date: 2026-07-26
approved_by: kennethenevoldsen (explicit instruction, 2026-08-12)
scheduled_for: 2026-08-12T14:30:00+02:00
expires: 2026-09-15
subject: webAI-Official/webAI-ColVec1.1-8b
verified: true
evidence: data.json
media: card-1-colvec11-vidore.png
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5010
  - https://github.com/embeddings-benchmark/results/pull/643
posted_on: 2026-08-12
url: https://bsky.app/profile/mteb.org/post/3msvapni2h62x
---

```
New on MTEB: webAI-Official/webAI-ColVec1.1-8b, a visual document retrieval model, takes 1st of 41 on ViDoRe(v3) at 64.95.

Its 4B sibling places 3rd at 63.90 — and both beat the lab's previous generation, which sits 6th and 7th.
```

## The claim

`ViDoRe(v3)` is 10 tasks of visual document retrieval — ranking page images against text
queries rather than ranking text against text. 41 models have complete coverage.

| rank | score | size | model |
|---:|---:|---:|---|
| **1** | **64.95** | 8.4B | `webAI-Official/webAI-ColVec1.1-8b` |
| 2 | 64.34 | 8B | `vultr/VultronRetrieverPrime-Qwen3.5-8B` |
| **3** | **63.90** | 4.5B | `webAI-Official/webAI-ColVec1.1-4b` |
| 6 | 63.00 | 9.4B | `webAI-Official/webAI-ColVec1-9b` |
| 7 | 62.22 | 4.5B | `webAI-Official/webAI-ColVec1-4b` |

The generational comparison is the part that is hard to argue with: same lab, same two
size classes, both improved, and the 4.5B ColVec1.1 now beats the 9.4B ColVec1 it
replaces. That is a within-lab observation, so it is untouched by who else submitted.

## Scope of the claim

"1st of 41" is the whole claim, and the qualifier does real work. ViDoRe(v3) has 41
models with complete coverage against 180 on `MTEB(eng, v2)` — visual document retrieval
is a much smaller field, and a rank in it is a rank among specialists who chose to enter.
The post says "of 41" for that reason and must keep saying it.

**The 4B is the folder's name and the 8B is the story.** The scanner filed this under the
4B because the PR title lists it first. Worth remembering that the candidate's name is not
evidence of anything.

## Why this one

Breadth (`AGENTS.md` #7). The account has published text retrieval and a text efficiency
frontier; visual document retrieval is a modality it has not covered, and the point of the
account is to signal that embeddings are not only about text.

## Notes

Contributed by zhanlunchang-webai; results submitted through `ResultCache.submit_results()`.
No Bluesky handle on file, so credit is plain text.

Numbers from the leaderboard API via `fetch.py`, complete coverage of all 10 ViDoRe(v3)
tasks, total parameters. Reproduced independently of the cross-board lookup used during
triage — same figures both ways.
