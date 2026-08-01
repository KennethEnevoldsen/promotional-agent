# Card design

Cards are HTML rendered to PNG. Each post owns its own `card.html` — there is no shared
template, deliberately: cards diverge before they converge, and extracting one from a
single example means bending later posts to fit a guess.

That makes this file the thing that carries forward. **The next card should inherit the
reasoning even when it does not inherit the code.**

## Why a card at all

A Bluesky post is 300 characters. Once a draft carries two model names, two scores, a
benchmark name and a credit line it is effectively full, with nothing left to explain why
anyone should care. Moving the numbers into the image frees the text to make the argument,
and gives the numbers more room than prose ever would.

The rest is ordinary: HTML is diffable, reviewable in a PR, data-driven from the results
repo, and consistent by construction because layout lives in CSS rather than in whoever
is making the image that day.

## How a card is put together

`fetch.py` writes *values* into the card's `#card-data` block. Every sentence a person
chose lives in a `COPY` object in the same file. Two reasons:

- `fetch.py` takes minutes. Copy stored there turns a one-word change into a
  minutes-long round trip; in `card.html` it is a three-second re-render.
- `fetch.py` should emit `60000000`, not `"models under 60M"`. A value can be checked
  against the leaderboard; a phrasing is an editorial choice and belongs with the others.

There is no intermediate `card.json`: the card carries its own data, so opening it in a
browser shows exactly what renders. A separate data file drifts to whatever placeholder
it was last hand-edited with, and then previewing shows a chart nobody published.

Cards are **1200×1200**. Feeds crop wide images; square keeps its full height. Only the
light PNG is kept — the image cannot follow the viewer's theme and you attach one image,
so a dark render is a duplicate of the same numbers. The dark CSS stays so `card.html`
reads properly in a dark browser.

## Choosing the form

| the data's job | form |
|---|---|
| score *given* size — an efficiency claim | scatter with a Pareto region |
| plain ordering, who is ahead | ranked bars |
| *where* a score comes from | radar over task types |
| a distribution across categories | beeswarm, one lane per category |
| change in a frontier over time | staircases, one per cohort |

They answer different questions, so the choice is editorial rather than cosmetic. A
ranking is the most legible and the least informative; a radar is the most interesting
and the least suited to carrying a headline.

## Rules that keep a chart honest

**Bars start at zero.** Truncating exaggerates. Arena's Elo charts start at 1,450, which
is conventional there, but on a 0-100 score it would misstate a 47-vs-58 gap as far
larger than it is.

**Missing results are dropped, never plotted as zero.** A model never evaluated on a
benchmark is not a model that scored badly, and conflating the two defames someone by
implication.

**Zero active parameters is a real value.** Static embedding models compute nothing per
token. `log(0)` has no position, so they get their own band behind an explicit axis
break, labelled `0 / static`. Nudging them to "0.1M" to fit the log scale erases the one
number that makes them interesting.

**A Pareto frontier is a staircase, not a line between points.** Joining frontier points
diagonally traces a curve through sizes at which no model has been trained. The staircase
says the true thing: at a given size you can have the best score achieved at or below it.

**The frontier is a shaded region with no line on its edge.** Everything inside is
dominated. The region's top edge *is* the frontier, so stroking it restates the shading.
It stops at the plot edges — it is a claim about the models plotted, not a background
wash.

**A card that makes a claim must carry its scope.** If the subtitle asserts "a new Pareto
frontier", the cohort that bounds it has to be visible on the image, because a screenshot
travels without the post. A claim cannot be corrected after posting: if it needs a
footnote to be true, it needs rewording instead.

## Colour

MTEB's own palette, from `scripts/generate_og_images_mpl.py` in the mteb repo:

| role | light | dark |
|---|---|---|
| brand blue | `#3d7bff` | `#5b8fff` |
| brand purple | `#a06bff` | `#a06bff` |
| context grey | `#b9b7b0` | `#6f6d67` |

Both brand colours clear 3:1 against the light and dark surfaces.

Use colour for **roles, not identities**: the subject in brand blue, the one comparison
worth naming in brand purple, everything else grey context. That is emphasis, not a
categorical palette — peers are context, not series competing for identity, which also
sidesteps the colourblind-safety problem rather than solving it.

Categorical colour is right only when the categories *are* the subject (openness tiers,
several models on a radar). Cap it at three.

Reserve texture for "different kind of thing": the size-class card marks its
out-of-class reference with a 45° hatch rather than a lighter fill, because a lighter
solid would read as "smaller number".

## Alt text

Generated by the card from the same data and read back out of the rendered page, so it
cannot disagree with the image. Written to `card.txt` beside the card.

This is not optional politeness. The numbers are the payload, and an image-only payload
is unreadable to screen readers and to anyone whose client fails to load it. It is also
where scope survives when a card has been decluttered — the cohort statement lives there
even when it is no longer printed on the image.

## Rendering

- **Chrome's `--screenshot` CLI flag hangs on macOS**, in both `--headless` and
  `--headless=new`. Killed after 2 minutes with no output, twice. Use Playwright with
  `channel="chrome"` — it drives the installed Chrome, so no browser download.
- **The SVG viewBox must match the plot box's real pixel size.** A fixed viewBox
  stretched to fit turns every circle into an ellipse.
