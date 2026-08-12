#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
#
# [tool.uv]
# exclude-newer = "2026-08-01T00:00:00Z"
# ///
"""Evidence for the mDenseOn/mLateOn post. Run from the repo root:

    uv run posts/3-review/mdenseon-mlateon/fetch.py

The claim is a within-lab, within-language comparison: does going multilingual cost
anything in English? BEIR is the only board where both the multilingual model and the
English-only model it extends have complete coverage, so it is the only board that can
answer that question. An earlier version of this script also reported the multilingual
models' own placement on CoIR and MTEB(Code, v1), where `LateOn`/`DenseOn` have no
complete-coverage row at all — but with no baseline there, that was context rather than a
claim, and the post is stronger without a second, weaker story competing with the real
one. Dropped rather than kept "for completeness".
"""

import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from mtebpost.cards import write_card_data

API = "https://mteb-leaderboard-backend.hf.space"
HERE = pathlib.Path(__file__).parent

# (multilingual model, the English-only model it extends)
PAIRS = [
    ("lightonai/mLateOn", "lightonai/LateOn"),
    ("lightonai/mDenseOn", "lightonai/DenseOn"),
]
COMPARISON_BOARD = "BEIR"


def board(name: str, attempts: int = 3) -> dict:
    url = f"{API}/v1/benchmarks/{urllib.parse.quote(name)}/scores"
    for i in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.load(r)
        except (TimeoutError, urllib.error.URLError):
            if i == attempts - 1:
                raise
    raise AssertionError("unreachable")


def complete(payload: dict) -> list[dict]:
    tasks = payload["tasks"]
    rows = [r for r in payload["rows"]
            if all(r["scoresByTask"].get(t) is not None for t in tasks)]
    rows.sort(key=lambda r: -r["meanTask"])
    return rows


def placement(payload: dict, model_name: str) -> dict | None:
    """Rank + score if the model has complete coverage; None if it doesn't — absence is
    a fact this script records rather than a gap it papers over."""
    rows = complete(payload)
    for i, r in enumerate(rows, 1):
        if r["model"]["name"] == model_name:
            return {"rank": i, "of": len(rows), "score": round(r["meanTask"] * 100, 2)}
    return None


def main() -> None:
    cmp_payload = board(COMPARISON_BOARD)
    n_cmp_tasks, n_cmp_complete = len(cmp_payload["tasks"]), len(complete(cmp_payload))

    comparisons = []
    for multi, base in PAIRS:
        m_place, b_place = placement(cmp_payload, multi), placement(cmp_payload, base)
        if not m_place or not b_place:
            raise SystemExit(
                f"{COMPARISON_BOARD}: expected both {multi} and {base} to have complete "
                f"coverage — got multi={m_place}, base={b_place}. The 'did not cost "
                "anything' claim depends on both being present; fix the claim, not this."
            )
        comparisons.append({
            "multilingual": multi, "multilingual_place": m_place,
            "base": base, "base_place": b_place,
            "delta": round(m_place["score"] - b_place["score"], 2),
        })

    evidence = {
        "generated": date.today().isoformat(),
        "source": f"{API}/v1/benchmarks/.../scores",
        "comparison_board": COMPARISON_BOARD,
        "n_comparison_tasks": n_cmp_tasks,
        "n_comparison_complete": n_cmp_complete,
        "comparisons": comparisons,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    write_card_data(HERE / "card.html", {
        "n_comparison_tasks": n_cmp_tasks,
        "n_comparison_complete": n_cmp_complete,
        "comparisons": comparisons,
    })

    print(f"{COMPARISON_BOARD}: {n_cmp_tasks} tasks, {n_cmp_complete} complete-coverage\n")
    for c in comparisons:
        mp, bp = c["multilingual_place"], c["base_place"]
        print(f"  {c['multilingual']:<20} rank {mp['rank']:>3} of {mp['of']}  "
              f"{mp['score']:>6}")
        print(f"  {c['base']:<20} rank {bp['rank']:>3} of {bp['of']}  {bp['score']:>6}  "
              f"(delta {c['delta']:+.2f})")


if __name__ == "__main__":
    main()
