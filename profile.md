# Account profile

Account-level copy: the handle, display name and bio. Not a post — this is the standing
description, and it changes rarely.

## The split

The bio answers **"should I follow this?"**. Posts carry **news**. Anything that is true
of every post belongs in the bio, not repeated in the feed.

That distinction is why there is no pinned introduction post. An explainer would mostly
restate the bio, and a first post is better spent on something that happened. See
`posts/rejected/introducing-this-account/` for the full reasoning and the condition that
would bring it back.

## Identity

**The account is MTEB**, not a companion or a named bot. The org is speaking, and the org
is accountable for what goes out — an agent drafts, people review, and the byline belongs
to the people either way.

So: **`mteb`**, not "MTEB Agent" or "MTEB Bot". Naming the tooling in the handle would
make the tool the subject, invite people to address it, and imply an autonomy it does not
have.

**Voice is "we", meaning the MTEB team.** Not first-person-singular — the agent is not a
character and should never be given one, because a character invites replies and this
account does not reply. "We" is for accountability, not warmth: if a number is wrong, we
got it wrong. It is not a licence for "we're excited to share".

## Bluesky

**Display name:** `MTEB`

**Bio** (Bluesky allows 256 characters):

```
News from the Massive Text Embedding Benchmark: new features, models, results, datasets and benchmarks.

Every number is recomputed from public results — check them yourself at leaderboard.mteb.org.

We don't reply here. Issues and PRs on GitHub.
```

**Link:** `https://leaderboard.mteb.org`

Three things that line does, in order of importance to someone deciding:

1. **What lands in the feed** — the concrete list, so the value is obvious without
   scrolling.
2. **That the numbers are checkable, and where.** This is the part worth spending
   characters on. Anyone can claim accuracy; pointing at the leaderboard invites the
   check, which is a different and stronger thing.
3. **That it does not converse** — stated plainly so silence reads as policy rather than
   as being ignored, and so nobody wastes a question here.

## What deliberately is not in the bio

- **"Drafted by an agent."** Currently the drafting is human-led with tooling, so the
  claim would overstate what happens. Revisit if that changes — it should be disclosed
  rather than discovered.
- **Cadence promises.** "Daily" or "weekly" is a commitment that will be broken in a
  quiet week and is not what anyone is deciding on.
- **Hashtags, emoji, follow-for-follow.** The account informs; it does not farm.

## LinkedIn

Same identity and voice. The bio can be longer, but it must say the same things — the
failure mode is two formats drifting into two personalities.

Per-post LinkedIn text lives in that post's `post.md` under `## LinkedIn`, not in a
separate file. See `CONTRIBUTING.md`.
