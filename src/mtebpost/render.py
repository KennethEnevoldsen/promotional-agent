#!/usr/bin/env python3
"""Render a post's card HTML to PNG.

    uv run visuals/render.py --card posts/<id>/card.html --out posts/<id>/card.png
    uv run visuals/render.py --card posts/<id>/card.html --mode dark --out /tmp/preview.png

The card is self-contained: `fetch.py` writes its numbers into the `#card-data` block,
and the copy lives in a `COPY` object beside it. So opening `card.html` in a browser
shows exactly what this produces — there is no separate data file that can drift from
the checked-in markup.

The only thing injected at render time is `mode`, merged into the existing card data
rather than replacing it, so dark and light come from one file.

Alt text is read back out of the rendered page (`window.__altText`) rather than
recomputed here — one definition, in the card, that cannot disagree with the image. It
is written next to the *card*, not the output, so `card.html` yields exactly one
`card.txt` no matter how many PNGs get rendered from it. A PNG cannot carry alt text and
Bluesky wants it as a separate field, which is why the sidecar exists at all.

`--mode dark` is for previewing: only one image can be posted, so the light render is
the artifact and a dark PNG would just be a second copy of the same numbers.

Uses the locally installed Chrome via Playwright's `channel="chrome"`, so there is no
browser download. Chrome's `--screenshot` CLI flag is deliberately not used: it hangs
on macOS in both the old and new headless modes.
"""

import argparse
import json
import pathlib
import re
import sys
import tempfile

from playwright.sync_api import sync_playwright

CARD_W, CARD_H = 1200, 1200  # square: social feeds crop wide images, and a
                             # square (or taller) card keeps its full height in-feed
SCALE = 2  # retina; produces a 2400x2400 png

BLOCK = re.compile(
    r'(<script type="application/json" id="card-data">)(.*?)(</script>)', re.S
)


def build_page(card: pathlib.Path, mode: str) -> str:
    """Return the card's HTML with `mode` merged into its data block."""
    html = card.read_text()
    m = BLOCK.search(html)
    if not m:
        sys.exit(f"{card}: no #card-data block found")
    data = json.loads(m.group(2))
    blob = json.dumps({**data, "mode": mode}, indent=2, ensure_ascii=False)
    return html[: m.start(2)] + "\n" + blob + "\n" + html[m.end(2) :]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card", required=True, help="path to the post's card.html")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=("light", "dark"), default="light")
    args = ap.parse_args()

    page_html = build_page(pathlib.Path(args.card), args.mode)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "card.html"
        src.write_text(page_html)
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            page = browser.new_page(
                viewport={"width": CARD_W, "height": CARD_H},
                device_scale_factor=SCALE,
            )
            page.goto(src.as_uri())
            page.wait_for_function("window.__altText !== undefined")
            page.screenshot(path=str(out))
            alt = page.evaluate("window.__altText")
            browser.close()

    # sidecar belongs to the card, not to this particular render
    alt_path = pathlib.Path(args.card).with_suffix(".txt")
    alt_path.write_text(alt + "\n")
    print(f"{out}  ({out.stat().st_size // 1024} KB)")
    print(f"{alt_path}  alt text")


if __name__ == "__main__":
    main()
