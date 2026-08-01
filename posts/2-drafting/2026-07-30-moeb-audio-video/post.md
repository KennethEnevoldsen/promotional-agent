---
id: 2026-07-30-moeb-audio-video
type: dataset_roundup
trigger_date: 2026-07-30
trigger: 18 MOEB/task PRs merged 2026-07-20..30 (cluster, no single event)
todo:
  - the count of 18 is from PR titles and has never been checked against the task registry
  - confirm each task is live rather than merged-but-awaiting-a-dataset-upload
  - no card; a roundup may not need one, but decide rather than default
expires: 2026-09-15
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5045
  - https://github.com/embeddings-benchmark/mteb/pull/5038
  - https://github.com/embeddings-benchmark/mteb/pull/5040
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
verified: false
media: none
thread: 3
---

```
1/ MTEB's audio and video coverage has grown substantially this month — 18 new tasks spanning music, speech, environmental sound, and video retrieval.
```

```
2/ Audio: AESDD (speech emotion), CASTELLA (moment retrieval), Song Describer (text↔music), Covers80 and SHS100K (cover song ID), UrbanSound8K, BirdCLEF, VimSketch (query by vocal imitation), SPEECH-COCO, SoundingEarth, CLD.
```

```
3/ Video: VSC2022 (copy detection), MomentSeeker (composed retrieval), MMVU, SEA-VL (multicultural VL for Southeast Asia), plus FLARE and MIAO task families.

Contributed by wissam-sib, dukesun99, and Rakshitha-Ireddi.
```

## Notes

This is the template for a quiet week — no single one of these 18 PRs is an announcement,
but together they are a real story about MTEB expanding past text. Verified: 18 MOEB-tagged
or modality-tagged task PRs merged between 2026-07-20 and 2026-07-30.

Credit splits evenly rather than falling to one person: wissam-sib (8 PRs), dukesun99
(8), Rakshitha-Ireddi (2). All three named in post 3 as plain text. None has a Bluesky
handle in `social-handles.yaml`, so none is @-mentioned.

At the one-a-day ceiling this cluster could also run as several posts instead of one
roundup — the music-retrieval tasks in particular (Song Describer, Covers80, SHS100K,
VimSketch) have enough of a shared story to stand alone. Kept as a roundup here to
demonstrate the type; worth revisiting.

**Check before posting:** FLARE and MIAO are described as "task families" because those
PRs each add several tasks. Confirm the exact count so "18" is defensible, and confirm
each task is actually live rather than merged-but-gated on a dataset upload.
