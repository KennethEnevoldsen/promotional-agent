# Card design

Cards are HTML rendered to PNG. Each post owns its own `card.html` — there is no shared
*runtime* template, deliberately: cards diverge before they converge, and extracting one
from a single example means bending later posts to fit a guess.

That makes this file the thing that carries forward. **The next card should inherit the
reasoning even when it does not inherit the code.**

**One exception, made on purpose once the repetition was real rather than anticipated:**
`model_addition` posts. By the fourth one (bekko, dinghy-law-family, colvec11-vidore,
mdenseon-mlateon) the same three shapes had reappeared with the same cohort-fairness
logic hand-rewritten each time — see `templates/model-release/` and
`mtebpost/model_release.py` below. This still copies a starting file into the post's own
folder rather than referencing anything at render time, so the "diverges before it
converges" property holds: editing a copied template can't affect another post's card.
Other post types (`dataset_roundup`, `state_of_field`, `benchmark_addition`) have not
converged on a shape yet and should stay bespoke until they do.

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

## The model-release template

For a `model_addition` post, `mtebpost/model_release.py` answers the three questions a
card needs before it can be built at all — who the fair peers are (full task coverage,
same benchmark), whether the subject sits on a size/score Pareto frontier, and whether
one peer is close enough to be a named rival — and `recommend_chart()` maps the answer
onto one of `templates/model-release/card-{pareto,radar,bars}.html`:

1. **pareto** if the subject is non-dominated among size-banded peers (nothing both
   smaller and higher-scoring exists) — the efficiency claim, when it's real, is
   usually the strongest available.
2. **radar**, else, if a same-or-larger peer scores within ~2 points — close enough
   that *where* the two differ is more informative than the gap in the mean.
3. **bars**, otherwise — always defensible, no story required. This is the fallback
   and, so far, the common case.

`recommend_chart()` is advice, not a decision: it can tell you a rival is close in
score, not that it's the rival worth naming (a same-lab prior generation may matter
more than the closest score — see colvec11-vidore). Print the reasoning, look at it,
then pick.

**Runs on the live leaderboard-backend API (`mtebpost/leaderboard_api.py`), not the
local `mteb` library.** The local package is version-pinned for reproducibility
(`pyproject.toml`'s `exclude-newer`), so it has no `ModelMeta` for anything registered
after that pin date — in practice most freshly-registered models, since mteb ships
fast. `malteos/most-embed-de`, the template's first real draft, is a concrete case:
registered 11 days after the pin, invisible to `mteb.get_model_meta()`, resolved fine
through the API. It is also just faster (no ~190s import, no per-model local result
load) — the reason colvec11-vidore/dinghy-law-family/mdenseon-mlateon already used this
API by hand before the template existed.

To draft with it: `cohort(subjects, benchmark)` pulls scores + size metadata for the
subject(s) and every full-coverage peer; pass `max_active=` to band by size instead of
ranking the whole registry (a Pareto claim needs the band, usually — though
`most-embed-de` turned out non-dominated across the *whole* field, band or not). If the
subject's own results don't cover a full registered benchmark — a fine-tune evaluated
on a hand-picked domain slice, the common case for a smaller lab's release — pass an
explicit task list instead of a benchmark name, scoped to what was actually run rather
than stretched to a benchmark nobody submitted to:

```python
from mtebpost.model_release import cohort, recommend_chart

coh = cohort(
    ["org/model-name"], ["Task1", "Task2", "Task3"],
    name="<post-specific name>",       # shows on the axis; omit only for <=3 tasks
    subsets={"Task2": "de"},           # pin any multi-language task to one subset —
)                                       # the API reports no score for partial coverage
rec = recommend_chart(coh)
print(rec.chart, rec.reason)  # decide, then call the matching *_card_data() builder
```

Then `pareto_card_data(coh)`, `radar_card_data(coh, roles)`, or `bars_card_data(coh,
prior=[...])` produces exactly the `#card-data` schema the matching template expects —
write it with `mtebpost.cards.write_card_data()`, same as any other card.
`pareto_card_data()` drops any peer with unknown active parameters itself (no honest
position on that axis); the other builders keep them, since a bars card can still size
rows by total parameters instead.

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

Generated by the card from the same data, read back out of the rendered page, and written
**into the card itself** as `<script type="text/plain" id="alt-text">`. So it cannot
disagree with the image, and a publisher can lift it out with a regex — no browser needed.

There is no `.txt` sidecar. A derived file beside a source file is a file that drifts,
which is the same reason there is no intermediate `card.json`.

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
