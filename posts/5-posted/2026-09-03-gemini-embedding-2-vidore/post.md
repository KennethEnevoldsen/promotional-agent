---
id: 2026-09-03-gemini-embedding-2-vidore
type: model_addition
trigger: mteb#5220 + results#679
trigger_date: 2026-08-18
scheduled_for: 2026-09-03T14:30:00+02:00
approved_by: kennethenevoldsen (explicit instruction, 2026-08-29)
expires: 2026-09-18
subject: google/gemini-embedding-2
verified: true
evidence: data.json
media: card-1-single-vector.png
thread: 2
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5220
  - https://github.com/embeddings-benchmark/results/pull/679
  - https://ai.google.dev/gemini-api/docs/embeddings
posted_on: 2026-09-03
url: https://bsky.app/profile/mteb.org/post/3mumnnl3wdw2s
---

Post 1 — card: `card-1-single-vector.png`

```
New on MTEB: google/gemini-embedding-2, which takes interleaved text, image, audio and video in one input.

Its first results are on ViDoRe(v2), visual document retrieval: 62.37, first of the 13 single-vector models with complete results.

Model and results by whybe-choi.
```

Post 2 — card: `card-2-board.png`

```
The other half of that board: 20 models score higher, and every one of them is a late-interaction retriever, storing a vector per page patch instead of one per document.

Of 50 models with complete results, gemini-embedding-2 is 21st.
```

## LinkedIn

The thread plus the thing neither card's headline says: the runner-up among single-vector
models is 69M parameters and 0.44 behind.

```linkedin
New on MTEB: google/gemini-embedding-2, now GA, which takes interleaved text, image, audio and video in a single input.

Its first merged results are on ViDoRe(v2) — four visual document retrieval tasks, ranking page images against text queries. It scores 62.37: first of the 13 single-vector models on that board, and 21st of all 50 models with complete results.

Every one of the 20 models above it is a late-interaction retriever. Those store a vector per page patch and score by summing per-patch maxima, which buys accuracy at the cost of an index that a general-purpose vector database is not built to hold. A single vector per page is a different engineering proposition, and the two are worth reading as separate columns rather than one ranking.

Worth its own line: the second single-vector model, nanovdr/NanoVDR-S-Multi, is 69M parameters and 0.44 behind.

Model and results by whybe-choi.
```

## The claim

`mteb#5220` registers `google/gemini-embedding-2` (GA), marks the March preview
superseded — the preview endpoint shut down on 2026-08-10 — and implements interleaved
text/image/audio/video input for it. `results#679`, same author, submits its first
results: `ViDoRe(v2)`, complete.

**Scope is `ViDoRe(v2)`, the registered 4-task benchmark, not the 14-task
`ViDoRe(v1&v2)`** — the model has 4 of those 14 and no comparable aggregate on them. The
four are `Vidore2BioMedicalLecturesRetrieval` (59.84), `Vidore2ESGReportsHLRetrieval`
(69.58), `Vidore2ESGReportsRetrieval` (61.86) and `Vidore2EconomicsReportsRetrieval`
(58.18); mean 62.37.

Of the 50 models with complete coverage, it places **21st** — and every one of the 20
above it is a **late-interaction** retriever, which stores a vector per page patch and
scores by summing per-patch maxima. `gemini-embedding-2` produces one vector per
document, and is the highest-scoring model on the board that does. The board splits 37
late-interaction to 13 single-vector:

| rank | score | model | architecture |
|---:|---:|---|---|
| 1 | 69.27 | `DataScience-UIBK/Argus-Colqwen3.5-9b-v0` | late-interaction |
| 20 | 62.47 | `VAGOsolutions/SauerkrautLM-ColQwen3-8b-v0.1` | late-interaction |
| **21** | **62.37** | **`google/gemini-embedding-2`** | **single-vector** |
| 22 | 61.93 | `nanovdr/NanoVDR-S-Multi` | single-vector |

Architecture is read from each model's registry `ModelMeta.model_type`, not inferred from
the "Col-" naming convention, and both claims — that everything above the subject is
late-interaction, and that no single-vector model scores higher — are assertions in
`fetch.py` rather than observations from its printout. The cohort is 37 late-interaction
models and 13 single-vector ones.

## Why a thread, and why this framing

The claim has two halves that no single ranking shows at once. Post 1 is the cohort the
model leads — all 13 single-vector models, so a reader can count the rows and check it.
Post 2 is the board it sits in, where 20 models score higher and every one of them is the
other architecture. Run alone, post 1 is the flattering half and post 2 is a rank with no
explanation; the two are one claim in two moves, which is what this account's threads are
for (see `2026-08-03-bekko-thread`).

Card 2 draws the ranks it does not list. A row marked 10 followed by a row marked 21 with
nothing between them invites the reader to guess what is in the gap, so the gap is a row
of its own: how many models, that they are all late-interaction, and the scores they run
between. Those numbers come from `fetch.py`, not from a hand-typed caption.

## Why not lead with the rank

"21st of 50" on its own is a number with little content: it invites the reader to conclude
the model is mid-field at visual document retrieval, when the thing the board actually
shows is a clean architectural split. Late interaction costs storage roughly in
proportion to page patches and needs a retrieval stack built for multi-vector search;
a single vector per page drops into any vector database. Those are different products,
and ranking them in one column without saying so is the misreading to avoid.

The reverse framing — "best single-vector model" alone — would be the flattering half of
the same fact. The post carries both halves in the order they matter: what it is, where
it lands, what is above it.

## Scope, and what is not claimed

- **Nothing about text.** This model's only merged results are these four tasks. It is
  not compared to `gemini-embedding-001` (no shared complete benchmark yet) and nothing
  is said about MTEB(Multilingual, v2) or MTEB(eng, v2), where it has no results.
- **Nothing about the modalities in the headline.** The interleaved audio and video
  support is what `mteb#5220` implements and is worth reporting as a capability; it is
  not measured by ViDoRe(v2), which is document images. The post says it takes that
  input, never that it is good at it.
- **The 4-task board is small, and the single-vector margin is thin.** Four retrieval
  tasks is a narrower base than the 10-task ViDoRe(v3) this account posted in August,
  and the margin over `nanovdr/NanoVDR-S-Multi` — a 69M-parameter open model — is 0.44.
  The claim is a placement on a stated board, not a general statement about single-vector
  visual retrieval. Card 1 shows that runner-up with its parameter count on the row
  directly below the subject, and the LinkedIn version says it in words, because a
  headline that omits it is doing the omitting on purpose.

## Notes

Credit: whybe-choi, author of both PRs. No Bluesky handle in `social-handles.yaml`, so
plain text, no @-mention.

**Card 2 does not draw rows 11-20 individually.** Twenty-one rows do not fit the canvas,
and ten near-identical Col- models would bury the subject. They are summarised in a
stand-in row instead of dropped silently — first draft of this card skipped them with no
marker at all, which is the version this note exists to prevent coming back.

`nanovdr/NanoVDR-S-Multi` at 61.93 with 69M parameters is arguably the more surprising
thing on card 1, and it is not this post's subject. Worth remembering as a candidate of
its own if the board holds.

**The axis carries the benchmark name and nothing else.** Both cards had a full sentence
where the axis label goes — benchmark, task count, cohort size, and a note about the gap
row, wrapping onto two lines. The scope still has to be on the image, since a screenshot
travels without the post, so it moved to a muted second line under the axis rather than
off the card. `templates/model-release/card-bars.html` now splits the same way
(`axis_label` for the name, `axis_note` for the scope), so the next bars card starts from
the two-tier version.

Two changes to shared code came out of drafting this, both worth knowing about because
they change what an older `fetch.py` would print if re-run:

- **`bars_card_data()` now writes each row's true board rank.** The template numbered
  rows by position, so a subject appended outside `top_n` printed rank 11 while lying
  21st — a wrong number, stated with the same confidence as a right one. Only this post
  has ever had a subject outside its card's top N, so no published card is affected.
- **`cohort()` no longer drops complete-coverage models whose parameter count is
  unpublished.** It filtered peers on `Entry.plottable` (complete *and* a known size),
  which silently shortened the board any rank is counted against — here from 50 to 33,
  removing `TomoroAI/tomoro-colqwen3-embed-8b` and `ApsaraStackMaaS/EvoQwen2.5-VL-Retriever-7B-v1`
  from above the subject and quietly promoting it from 21st to 17th. A model with no
  published size is perfectly comparable by score; only a size *axis* needs a size, and
  `pareto_card_data()` and `max_active` each enforce that themselves. The custom-task-list
  branch always split on coverage alone, so this also makes the two agree.

**Scheduled for 2026-09-03, 14:30+02:00**, approved by kennethenevoldsen on
2026-08-29 ("feel free to schedule all of them now"). Two days after the Slovak post and
well inside `expires: 2026-09-18`.
