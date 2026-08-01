"""Write query results into a post's card.html.

`fetch.py` injects its data directly into the card's `#card-data` block rather than
writing a separate card.json. That keeps one copy of the truth: opening `card.html` in
a browser shows exactly what `render.py` will produce, because it is the same file with
the same data. With an intermediate JSON, the checked-in card drifts to whatever
placeholder it was last hand-edited with, and previewing it shows a chart nobody
published.

Only data goes through here. Every human-written sentence lives in the `COPY` object at
the top of the card.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

BLOCK = re.compile(
    r'(<script type="application/json" id="card-data">)(.*?)(</script>)', re.S
)


def write_card_data(card_html: pathlib.Path, data: dict) -> None:
    html = card_html.read_text()
    blob = json.dumps(data, indent=2, ensure_ascii=False)
    html, n = BLOCK.subn(lambda m: m.group(1) + "\n" + blob + "\n" + m.group(3), html, count=1)
    if not n:
        sys.exit(f"{card_html}: no #card-data block to write into")
    card_html.write_text(html)
