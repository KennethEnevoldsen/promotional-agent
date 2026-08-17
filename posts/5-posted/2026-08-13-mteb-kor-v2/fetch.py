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
"""Evidence for the MTEB(kor, v2) post. Run from the repo root:

    uv run posts/3-review/mteb-kor-v2/fetch.py

This is a benchmark-replacement post, not a model-ranking one: the claim is about the
board itself (v1 -> v2, 6 tasks -> 20, 4 task types -> 6). So the evidence this script
asserts is different from a ranking post's:

  1. v2's task set is a strict superset of v1's — checked, not assumed, because
     the PR body's own description of what it did turned out to be wrong (see below).
  2. the two new task types (clustering, pair classification) did not exist on v1 at all.
  3. the size-bucket Pareto — best model in >5B / 1-5B / 500M-1B / <500M — on each board,
     and whether the winner's identity changes between them. This is the leaderboard's own
     framing (leaderboard.mteb.org buckets the same way), and the question it answers —
     does a broader benchmark change who's best — is a sharper claim than "who submitted
     alongside this PR", which was the first draft of this evidence and was really a fact
     about the pull request rather than about the benchmark.

The PR body says "MTEB(kor, v1) task expansion... from 6 to 19 tasks." Both halves are
wrong: v1 is untouched at 6 tasks on the live board, and the live v2 board has 20 tasks,
not 19. This script checks the live boards rather than trusting that description, which is
the whole reason it exists (AGENTS.md #3 — a contributor's summary of their own PR is a
claim to verify, never a fact to repeat).
"""

import json
import pathlib
import urllib.parse
import urllib.request
from datetime import date

from mtebpost.cards import write_card_data

API = "https://mteb-leaderboard-backend.hf.space"
V1, V2 = "MTEB(kor, v1)", "MTEB(kor, v2)"
HERE = pathlib.Path(__file__).parent

# Same buckets leaderboard.mteb.org uses. Order is largest to smallest, matching how the
# card reads left to right. Plain text — any HTML escaping is the card's job at render
# time, not something baked into the evidence file.
BUCKETS = [(">5B", 5, None), ("1-5B", 1, 5), ("500M-1B", 0.5, 1), ("<500M", 0, 0.5)]


def board(name: str) -> dict:
    url = f"{API}/v1/benchmarks/{urllib.parse.quote(name)}/scores"
    with urllib.request.urlopen(url, timeout=180) as r:
        return json.load(r)


def task_types(payload: dict) -> list[str]:
    # Pulled from the /scores payload itself, not the /v1/benchmarks list — v1 was
    # dropped from that list once superseded, even though its /scores endpoint still
    # answers. Reading types from the same response that gives the task set means one
    # fewer place this could disagree with itself.
    return sorted(payload.get("simplifiedTaskTypes") or payload.get("taskTypes") or [])


def type_counts(payload: dict) -> dict[str, int]:
    """Tasks per type, from `tasksMeta` — the per-task type is not derivable from the
    bare `tasks` name list, and this is the field that actually carries it."""
    counts: dict[str, int] = {}
    for t in payload["tasksMeta"]:
        counts[t["type"]] = counts.get(t["type"], 0) + 1
    return counts


def complete_rows(payload: dict) -> list[dict]:
    tasks = payload["tasks"]
    rows = [r for r in payload["rows"]
            if all(r["scoresByTask"].get(t) is not None for t in tasks)]
    rows.sort(key=lambda r: -r["meanTask"])
    return rows


def bucket_of(params_b: float | None) -> str | None:
    if params_b is None:
        return None
    for name, lo, hi in BUCKETS:
        if hi is None:
            if params_b >= lo:
                return name
        elif lo <= params_b < hi:
            return name
    return None


def intersection_pareto(v1: dict, v2: dict) -> tuple[list[str], dict[str, dict], dict[str, dict]]:
    """Restrict the size-bucket comparison to models with complete coverage on BOTH
    boards, so "did the leader change" isn't confounded by a model that simply never ran
    the new tasks — that was the first version of this check, and a v1 leader dropping out
    because it never attempted clustering or NLI is a coverage fact, not a capability one.

    Because v2's task set is a strict superset of v1's, complete v2 coverage implies
    complete v1 coverage — so this intersection is exactly the v2-complete set. Verified
    here rather than assumed, since the whole analysis depends on it.
    """
    v1_by_name = {r["model"]["name"]: r for r in complete_rows(v1)}
    v2_by_name = {r["model"]["name"]: r for r in complete_rows(v2)}
    if not set(v2_by_name) <= set(v1_by_name):
        raise SystemExit(
            "a model has complete v2 coverage but not v1 — the superset assumption this "
            "check relies on does not hold; investigate before trusting the comparison"
        )
    return sorted(set(v2_by_name)), v1_by_name, v2_by_name


def bucket_pareto(intersection: list[str], v1_by: dict, v2_by: dict) -> list[dict]:
    by_bucket: dict[str, list[str]] = {}
    for name in intersection:
        b = bucket_of(v1_by[name]["model"].get("totalParamsB"))
        if b:
            by_bucket.setdefault(b, []).append(name)
    rows = []
    for name, _, _ in BUCKETS:
        names = by_bucket.get(name, [])
        if not names:
            rows.append({"bucket": name, "v1": None, "v2": None, "changed": False, "n": 0})
            continue
        v1_best = max(names, key=lambda n: v1_by[n]["meanTask"])
        v2_best = max(names, key=lambda n: v2_by[n]["meanTask"])
        rows.append({
            "bucket": name,
            "v1": {"model": v1_best, "score": round(v1_by[v1_best]["meanTask"] * 100, 2)},
            "v2": {"model": v2_best, "score": round(v2_by[v2_best]["meanTask"] * 100, 2)},
            "changed": v1_best != v2_best,
            "n": len(names),
        })
    return rows


def main() -> None:
    v1, v2 = board(V1), board(V2)
    v1_tasks, v2_tasks = set(v1["tasks"]), set(v2["tasks"])

    if not v1_tasks <= v2_tasks:
        raise SystemExit(
            f"v2 is not a superset of v1 — missing {v1_tasks - v2_tasks}. "
            "The 'strict superset' claim in post.md depends on this; fix the claim, "
            "not this check."
        )
    new_tasks = sorted(v2_tasks - v1_tasks)

    v1_types, v2_types = task_types(v1), task_types(v2)
    new_types = sorted(set(v2_types) - set(v1_types))
    v1_counts, v2_counts = type_counts(v1), type_counts(v2)
    if sum(v1_counts.values()) != len(v1_tasks) or sum(v2_counts.values()) != len(v2_tasks):
        raise SystemExit("tasksMeta type counts do not sum to the task list length")
    by_type = [
        {"type": t, "v1": v1_counts.get(t, 0), "v2": v2_counts.get(t, 0)}
        for t in sorted(set(v1_types) | set(v2_types))
    ]

    intersection, v1_by, v2_by = intersection_pareto(v1, v2)
    bucket_rows = bucket_pareto(intersection, v1_by, v2_by)

    evidence = {
        "intersection_size": len(intersection),
        "intersection_note": (
            "models with complete coverage on both boards — exactly the v2-complete set, "
            "since v2's tasks are a superset of v1's. Restricting to this set means a "
            "bucket 'changing' can only reflect the extra tasks, never a model that simply "
            "never ran them."
        ),
        "generated": date.today().isoformat(),
        "source": f"{API}/v1/benchmarks/.../scores",
        "v1": {"benchmark": V1, "n_tasks": len(v1_tasks), "task_types": v1_types,
               "n_complete": len(complete_rows(v1))},
        "v2": {"benchmark": V2, "n_tasks": len(v2_tasks), "task_types": v2_types,
               "n_complete": len(complete_rows(v2))},
        "new_tasks": new_tasks,
        "new_task_types": new_types,
        "by_type": by_type,
        "pr_claim_check": {
            "claimed": "MTEB(kor, v1) task expansion, from 6 to 19 tasks",
            "actual": f"v1 unchanged at {len(v1_tasks)} tasks; new benchmark v2 has "
                      f"{len(v2_tasks)} tasks",
            "verdict": "wrong on both counts",
        },
        "size_pareto": bucket_rows,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    write_card_data(HERE / "card-1-mteb-kor-v2.html", {
        "n_complete_v1": len(complete_rows(v1)),
        "n_complete_v2": len(complete_rows(v2)),
        "intersection_size": len(intersection),
        "by_type": by_type,
        "buckets": bucket_rows,
    })

    print(f"{V1}: {len(v1_tasks)} tasks, {len(v1_types)} types, "
          f"{len(complete_rows(v1))} complete-coverage models")
    print(f"{V2}: {len(v2_tasks)} tasks, {len(v2_types)} types, "
          f"{len(complete_rows(v2))} complete-coverage models")
    print(f"v2 superset of v1: {v1_tasks <= v2_tasks}")
    print(f"new task types: {new_types}")
    print("by type (v1 -> v2):")
    for row in by_type:
        print(f"  {row['type']:<20} {row['v1']:>2} -> {row['v2']:>2}")
    print(f"\nintersection (complete on both v1 and v2): {len(intersection)} models")
    print("size-bucket Pareto within the intersection, v1 scoring -> v2 scoring:")
    for row in bucket_rows:
        a = f"{row['v1']['model']} ({row['v1']['score']})" if row["v1"] else "no entrant"
        b = f"{row['v2']['model']} ({row['v2']['score']})" if row["v2"] else "no entrant"
        mark = " CHANGED" if row["changed"] else ""
        print(f"  {row['bucket']:<9} n={row['n']:<2} {a}  ->  {b}{mark}")


if __name__ == "__main__":
    main()
