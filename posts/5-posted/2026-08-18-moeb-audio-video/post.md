---
id: 2026-08-18-moeb-audio-video
type: dataset_roundup
trigger: 16 MOEB/task PRs merged 2026-07-20..30 (cluster, no single event)
trigger_date: 2026-07-30
approved_by: kennethenevoldsen (explicit instruction, 2026-08-12)
scheduled_for: 2026-08-18T14:30:00+02:00
expires: 2026-09-15
verified: true
evidence: data.json
media: card-1-roundup.png
thread: 3
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5045
  - https://github.com/embeddings-benchmark/mteb/pull/5038
  - https://github.com/embeddings-benchmark/mteb/pull/5001
  - https://github.com/embeddings-benchmark/mteb/pull/4991
  - https://github.com/embeddings-benchmark/mteb/pull/4984
  - https://github.com/embeddings-benchmark/mteb/pull/4988
  - https://github.com/embeddings-benchmark/mteb/pull/4978
  - https://github.com/embeddings-benchmark/mteb/pull/4985
  - https://github.com/embeddings-benchmark/mteb/pull/4967
  - https://github.com/embeddings-benchmark/mteb/pull/4963
  - https://github.com/embeddings-benchmark/mteb/pull/4964
  - https://github.com/embeddings-benchmark/mteb/pull/4965
  - https://github.com/embeddings-benchmark/mteb/pull/4966
  - https://github.com/embeddings-benchmark/mteb/pull/5023
  - https://github.com/embeddings-benchmark/mteb/pull/5025
  - https://github.com/embeddings-benchmark/mteb/pull/4986
posted_on: 2026-08-18
url: https://bsky.app/profile/mteb.org/post/3mtebm423fj2g
---

```
1/ MTEB's audio and video coverage grew substantially this month — 25 new tasks across 16 pull requests, spanning music, speech, environmental sound, and video retrieval. 10 of the 16 cite a published paper.
```

```
2/ Audio (18 tasks): AESDD, CASTELLA, Song Describer, Covers80, SHS100K, UrbanSound8K, BirdCLEF, VimSketch, SPEECH-COCO, SoundingEarth, CLD, MIAO — several as bidirectional retrieval pairs, which is most of where 16 PRs became 25 tasks.
```

```
3/ Video (7 tasks): VSC2022, MomentSeeker, MMVU, plus FLARE (3 tasks).

Contributed by dukesun99 (14 tasks), wissam-sib (9), and Rakshitha-Ireddi (2).
```

## The claim

25 task classes, verified against the merged diffs rather than counted from PR titles or
hand-typed labels: each PR's diff was checked for task classes actually defined
(`class X(AbsTask...)`), confirmed imported into its package `__init__.py` (a class that
is defined but never imported is not reachable through `mteb.get_task()`), and its
modality read from `TaskMetadata.modalities` rather than assigned by hand.

| | tasks |
|---|---:|
| audio | 18 |
| video | 7 |
| **total** | **25** |

10 of the 16 pull requests cite a published paper (an arXiv reference on at least one of
their tasks); the rest cite a GitHub repo, Zenodo, a university page, or a dataset card.

## What must not be claimed

**This post's own number moved twice, and both moves are worth being explicit about.**

The first draft said **18** — counted from PR titles, never checked against anything, not
even its own 17-PR source list. Counting task classes actually defined in the diffs gives
**27**: most of these PRs register more than one task (FLARE adds three, MIAO adds two,
eight more add a bidirectional pair like `A2I`/`I2A`), so one PR is not one task.

Rebuilding the modality split from `TaskMetadata.modalities` — rather than the hand-typed
label the second draft still carried — found two more problems with that 27:

- **`MIAO` was tagged "video".** Its two tasks (`MIAOA2IRetrieval`, `MIAOI2ARetrieval`)
  have `modalities: ["audio", "image"]` — no video modality at all. Moved to audio.
- **`SEA-VL` (mteb#5040) has no audio or video modality on either task** — both are
  `["text", "image"]`. It is a real PR with real tasks, and it does not belong in a post
  about audio and video coverage, so it is excluded from the count and the source list
  rather than stretched to fit. Its two tasks are the entire gap between 27 and 25.

## Notes

This is the template for a quiet week — no single one of these 16 PRs is an announcement,
but together they are a real story about MTEB expanding past text. (Internal note, not
for the post: an earlier draft of this card's subtitle repeated this exact sentence to
readers, which is a description of *our* editorial process, not a fact about MTEB. Cut
from the card; see `CONTRIBUTING.md` — audience-facing text only states what happened.)

Credit is by task count, not PR count, because the two disagree here: dukesun99 opened
8 PRs contributing 14 tasks, wissam-sib opened 7 PRs contributing 9 tasks (two of the
original 11 were SEA-VL, now excluded), and Rakshitha-Ireddi opened 2 PRs contributing 2
tasks. All three named in post 3 as plain text. None has a Bluesky handle in
`social-handles.yaml`, so none is @-mentioned.

**Card redesign.** The first version of the card was a sorted bar chart, one bar per PR,
length = task count. That axis measures an implementation detail — how many
bidirectional-pair task classes a PR happened to split into — not anything a reader would
care about, and was dropped for that reason. In its place: one featured task per
subdomain (music, speech, environmental sound, cross-modal audio-scene, video retrieval,
video QA), each with its own real description and an APA citation for its source paper,
plus a header stat for how many of the 16 PRs cite a published paper. Subdomain grouping
is an editorial judgment, not a field pulled from the API — recorded as such in
`fetch.py` — but the modality split, task count, and paper count are all computed.

**One card, numbered for the thread.** This is a 3-part thread; posts 2/3 and 3/3 are
text-only, and only post 1/3 carries this card. `mteb-publish` still needs the card
named `card-1-roundup.png` rather than plain `card.png` — `publish.py`'s `card_for()`
matches `card-N-*.png` to post N by filename, so the number identifies *which* part of
the thread the image belongs to even when the other parts have none. The original
`card.png`/`card.html` (no number) silently blocked every scheduled publish run from
2026-08-16 21:28 onward, because `card_for()` had nothing to match to post 1 by that
name; `card_for()` was then relaxed so a thread part with no numbered card of its own
is treated as deliberately image-less, the same as `media: none`, instead of an error.

At the one-a-day ceiling this cluster could also run as several posts instead of one
roundup — the music-retrieval tasks in particular (Song Describer, Covers80, SHS100K)
have enough of a shared story to stand alone. Kept as a roundup here to demonstrate the
type; worth revisiting.
