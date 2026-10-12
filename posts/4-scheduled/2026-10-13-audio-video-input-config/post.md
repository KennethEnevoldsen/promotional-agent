---
id: 2026-10-13-audio-video-input-config
type: feature_release
trigger: mteb#5454 (fix: audio video input config), first released in mteb 2.24.4
trigger_date: 2026-10-10
approved_by: kennethenevoldsen (explicit instruction, 2026-10-12)
scheduled_for: 2026-10-13T14:30:00+02:00
expires: 2026-11-07
verified: true
evidence: data.json
media: card-1-before-after.png
thread: 3
sources:
  - https://github.com/embeddings-benchmark/mteb/pull/5454
  - https://github.com/embeddings-benchmark/mteb/releases/tag/2.24.4
  - https://docs.mteb.org/whats_new/
  - https://github.com/embeddings-benchmark/mteb/issues/5460
---

```
1/ When we built MAEB, we cut audio at 30 seconds per clip to keep evaluation affordable. Many models support much longer audio, and at least 16 of our audio tasks have longer clips (up to 21 minutes), so those models were only scored on the start of each recording.
```

```
2/ From mteb 2.24.4, each audio and video model uses the limits its authors set instead: its own maximum clip length, sampling rate and number of video frames. This is what we already do for text, where each model reads up to its own maximum input length.
```

```
3/ Because scores change, we will rerun the audio and video models on the leaderboard with the new settings.

If you submit new audio or video results, please use mteb 2.24.4 or later.

Work by AdnanElAssadi.
```

## LinkedIn

The Bluesky thread as one post, word for word. The only difference is the credit line,
which tags Adnan on LinkedIn (see Notes).

```linkedin
When we built MAEB, we cut audio at 30 seconds per clip to keep evaluation affordable. Many models support much longer audio, and at least 16 of our audio tasks have longer clips (up to 21 minutes), so those models were only scored on the start of each recording.

From mteb 2.24.4, each audio and video model uses the limits its authors set instead: its own maximum clip length, sampling rate and number of video frames. This is what we already do for text, where each model reads up to its own maximum input length.

Because scores change, we will rerun the audio and video models on the leaderboard with the new settings.

If you submit new audio or video results, please use mteb 2.24.4 or later.

Work by @Adnan El Assadi.
```

## The claim

Computed in `fetch.py` rather than taken from the PR. The post text no longer states the
model count (kennethenevoldsen, 2026-10-12: no exact number); it is kept here as the
scope of the planned rerun.

| | |
|---|---:|
| models with ≥1 result on an audio- or video-modality task | **93** |
| … of which have any result computed with mteb < 2.24.4 | **93** |
| … of which have any result computed with mteb ≥ 2.24.4 | 0 |
| wrapper modules whose code changed (AST diff, comments and docstrings ignored) | 48 |
| modules that only gained a source comment | 17 |

Results repo at `6661f313`, read 2026-10-12. Every result file carries the `mteb_version`
that produced it; none of the 93 had a missing or unparsable version. 75 of the 93 have
audio results, 37 have video results (some both).

**2.24.4 is the first release containing the merge commit** (`5621901c`):
`compare/2.24.3...5621901c` is "ahead", `compare/2.24.4...5621901c` is "behind".

The 48/17 split is not used in the post text, but it is why the post does not say "the
PR changed 66 model files": a third of those only gained a comment citing a source.

**"At least 16 audio tasks have longer clips, up to 21 minutes."** From each task's own
descriptive statistics shipped with mteb 2.24.10, counting **evaluation splits only**:
16 audio tasks have a clip over 30 s. The longest is INatSounds at 1,271.6 s (21.2 min),
then BirdCLEF at 491 s, then VoxPopuliAccentID at 117 s; the full list is in `data.json`.
Counting train splits too (classification tasks embed them to fit their probe, and the
cap truncated them just the same) gives 19. The post uses the conservative 16 and says
"at least". 75 audio tasks had statistics available; the count is not presented as a
share of all audio tasks, because tasks without shipped stats are not in the denominator.

**"Many audio models … were only ever shown the first 30 seconds."** Checked in the code
at the parent commit: the wav2vec2 wrapper alone defaulted to `max_audio_length_seconds:
float = 30.0` and truncated with `max_length=30 s × sampling_rate` across ten checkpoints;
22 changed wrapper files had a 30 s default. Not every one was applied (Audio Flamingo's
was stored and never used, which is why it is not the example), so the post says "many",
not "most" or "all".

**"We cut audio at 30 seconds … to keep evaluation affordable."** The reason for the
cap is from kennethenevoldsen (maintainer), 2026-10-12, not from the code; the old wrappers
carry no comment explaining it. Framing the post around that decision, rather than around
the list of changed parameters, was also his call after two drafts read like a changelog.

## What must not be claimed

- **Not "every model's score changes."** The post says scores change and that we will
  rerun the audio and video models, both true. Whether a *particular* model's score moves
  depends on its wrapper and on the clip lengths in each task. The shared frame sampler
  (`FramesCollator.resample_video`) changed for every video path in mteb, so for video
  it is close to all of them; for audio it is per wrapper. MTEB's own release note says
  earlier results "are not comparable", which is the claim this post rests on.
- **No before/after scores.** The PR and its commit message quote some (e.g. CNN14 on
  GunshotTriangulation, LAION-CLAP on FSDD). They are contributor measurements on
  single tasks, not recomputed, and the reruns that would let us recompute them do not
  exist yet (0 models above).
- **Not "v2.25".** `docs/whats_new.md` heads this section "New in v2.25", but the change
  shipped as a `fix:` in 2.24.4 and no 2.25 exists (latest is 2.24.10). The post names
  the version that actually contains it. See Notes.

## Notes

**Why a patch release gets a feature post.** CONTRIBUTING says patch releases are not
features. This one is the exception it allows for: a change whose consequence a user
would not guess from the title. It was merged as `fix:`, but it invalidates every audio
and video result on the leaderboard, and isaac-chung asked on the PR whether there was a
way to announce it. Requested by kennethenevoldsen on 2026-10-12.

**Why a thread, and why this order.** The first draft led with what changed (clip
length, sampling rate, frame count) and was rejected as reading like a diff: a reader
could not tell what was wrong, why it was changed or what it meant for them. The thread
now answers those three questions in order — 1/ what was wrong, with a concrete number;
2/ what we changed and the principle behind it (run each model as its authors intended,
so a capability is credited rather than normalised away — the reasoning in mteb#5460);
3/ what it means and what to do. The per-model list lives behind the What's New link.

**Credit.** AdnanElAssadi wrote the PR. Samoed and isaac-chung reviewed it substantially
(isaac-chung's reviews checked the frame-sampling change and pushed for tests, a safer cap on long clips and consistent cap validation), but
review is not credited in posts. Searched 2026-10-12: no Bluesky handle on his GitHub profile or personal site
(X and LinkedIn only), recorded as `bluesky: null` in `social-handles.yaml`. Plain-text
credit, no @-mention. On LinkedIn he is tagged (`@Adnan El Assadi`, kennethenevoldsen's instruction, 2026-10-12;
profile in `social-handles.yaml`). When pasting, select him from LinkedIn's mention
dropdown so it links to linkedin.com/in/adnan-el-assadi-3b415b365 rather than staying plain text.

**Decisions for the reviewer:**

1. **The leaderboard right now.** Resolved: kennethenevoldsen confirmed on 2026-10-12
   that existing models will be rerun under the new settings, and part 3 says so ("we will
   rerun the audio and video models"). No date is given in the post, because none was given to us.
2. **The docs heading.** "New in v2.25" in `docs/whats_new.md` does not match any release.
   Either cut 2.25 (isaac-chung suggested a `feat:` bump on the PR) or rename the heading.
   If 2.25 is cut before this goes out, the post can say "mteb 2.25". The rerun advice
   stays correct either way.
3. **Card.** Text-only as drafted. A card could show a handful of before/after configs
   (e.g. Audio Flamingo 3 30 s → 600 s, wav2vec2 30 s → full clip, GVE 32 → 8 frames),
   each verifiable from the code at `5621901c`. Worth it if you want the change to read
   at a glance; the text stands on its own without it.

**Interaction with other posts.** `2-drafting/languagebind-omni` reports MVEB(beta)
scores computed before 2.24.4, and LanguageBind is one of the wrappers changed here
(random flip removed, audio crops seeded). Its numbers need recomputing after a rerun
before it can move. The same applies to any audio/video candidate in `1-candidates`.
