#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mtebpost"]
#
# [tool.uv.sources]
# mtebpost = { path = "../../..", editable = true }
# ///
"""Evidence for the MOEB audio/video roundup. Run from the repo root:

    uv run posts/3-review/moeb-audio-video/fetch.py

No leaderboard score here — this is a coverage-growth story, and everything checkable
comes from the merged diffs on GitHub, not from `mteb-leaderboard-backend`.

Three things this script verifies that an earlier draft got wrong by hand-labelling
instead of reading the code:

1. **Task count.** The original draft said "18", counted from PR titles. The real number
   is derived from `class X(AbsTask...)` definitions actually present and imported — see
   the module-level docstring history in git blame if you want the full story; the count
   that survives review is computed fresh below, not carried over.
2. **Modality.** Each task's `TaskMetadata.modalities` field is the source of truth, not
   a per-PR label typed by hand. Hand-labelling is exactly how `MIAO` (image+audio) ended
   up called "video", and how `SEA-VL` (image+text, no audio or video modality at all)
   ended up counted toward an "audio and video" claim it does not support. SEA-VL is
   excluded from this post's scope for that reason — its PR is real and its tasks are
   real, but they are not audio or video tasks, and this account does not stretch a claim
   to keep a number round.
3. **Provenance.** "These are real, documented datasets" is a checkable claim, not a
   vibe: whether a task's `reference` resolves to an arXiv paper, and the paper's own
   author/year, both come from the task's own metadata.
"""

import json
import pathlib
import re
import subprocess
import sys
from datetime import date

from mtebpost.cards import write_card_data

REPO = "embeddings-benchmark/mteb"
HERE = pathlib.Path(__file__).parent

# (PR number, short label, editorial subdomain grouping)
#
# Modality (audio/video) is derived from each task's own `modalities` field — never
# hand-typed here, after MIAO/SEA-VL showed why that goes wrong. Subdomain IS an
# editorial grouping (there is no API field for "this is a music-retrieval task"), used
# only to pick one featured example per corner of the roundup on the card. It is a
# judgment call, not a fact, and is labelled as such in the evidence file.
#
# SEA-VL (mteb#5040) is deliberately absent: `SeaVLCrawlingT2IRetrieval` and
# `SeaVLCrawlingI2TRetrieval` have modalities ["text", "image"] — no audio, no video.
# It doesn't support this post's claim and isn't stretched to fit it.
PRS = [
    (5045, "SHS100K", "music"),
    (5038, "MMVU", "video-qa"),
    (5001, "MIAO", "audio-scene"),
    (4991, "FLARE", "video-retrieval"),
    (4984, "CASTELLA", "audio-scene"),
    (4988, "Song Describer", "music"),
    (4978, "AESDD", "speech"),
    (4985, "VSC2022", "video-retrieval"),
    (4967, "MomentSeeker", "video-retrieval"),
    (4963, "VimSketch", "speech"),
    (4964, "SPEECH-COCO", "speech"),
    (4965, "CLD", "audio-scene"),
    (4966, "SoundingEarth", "environmental"),
    (5023, "BirdCLEF", "environmental"),
    (5025, "UrbanSound8K", "environmental"),
    (4986, "Covers80", "music"),
]

# One featured task per subdomain, for the card. Picked for how well the description
# alone conveys what the task measures, not for score, size, or alphabetical order.
FEATURED = {
    "music": "SongDescriberT2ARetrieval",
    "speech": "SpeechCocoA2IRetrieval",
    "environmental": "SoundingEarthA2IRetrieval",
    "audio-scene": "CASTELLAAMRRetrieval",
    "video-retrieval": "MomentSeekerTI2VRetrieval",
    "video-qa": "MMVUVideoCentricQA",
}

CLASS_BLOCK_RE = re.compile(r"\+class (\w+)\(Abs(\w+)\):.*?(?=\n\+class |\Z)", re.S)
INIT_DIFF_RE = re.compile(r"diff --git a/(\S*__init__\.py) .*?\n(?:.*?\n)*?(?=diff --git|\Z)", re.S)


def _gh(args: list[str], attempts: int = 3) -> str:
    last_err = ""
    for _ in range(attempts):
        p = subprocess.run(["gh", *args], capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout
        last_err = p.stderr.strip()
    sys.exit(f"gh {' '.join(args)} failed after {attempts} attempts: {last_err}")


def pr_diff(number: int) -> str:
    return _gh(["pr", "diff", str(number), "--repo", REPO])


def pr_meta(number: int) -> dict:
    return json.loads(_gh(["pr", "view", str(number), "--repo", REPO,
                           "--json", "title,mergedAt,state,author"]))


def imported_names(diff: str) -> set[str]:
    names = set()
    for m in INIT_DIFF_RE.finditer(diff):
        for line in m.group(0).splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                names.update(re.findall(r'"(\w+)"', line))
                names.update(re.findall(r",\s*(\w+)\s*[,)]", line))
    return names


def apa_cite(author_field: str, year: str) -> str:
    """'Last, First and Last, First' or 'First Last and First Last' -> 'Last et al. (Year)'."""
    segs = [s.strip() for s in author_field.split(" and ")]
    lastnames = [s.split(",")[0].strip() if "," in s else s.split()[-1] for s in segs]
    if len(lastnames) == 1:
        return f"{lastnames[0]} ({year})"
    if len(lastnames) == 2:
        return f"{lastnames[0]} & {lastnames[1]} ({year})"
    return f"{lastnames[0]} et al. ({year})"


def field(block: str, name: str) -> str | None:
    m = re.search(rf'{name}="([^"]+)"', block)
    return m.group(1) if m else None


def description_of(block: str) -> str:
    m = re.search(r"description=(.*?)\n\+\s+reference=", block, re.S)
    if not m:
        return ""
    return "".join(re.findall(r'"([^"]*)"', m.group(1))).strip()


def task_info(name: str, kind: str, block: str, diff: str) -> dict:
    mods = re.search(r"modalities=\[(.*?)\]", block)
    modalities = re.findall(r'"(\w+)"', mods.group(1)) if mods else []
    ref = field(block, "reference")
    if ref is None:
        var = re.search(r"reference=(\w+)", block)
        if var:
            m2 = re.search(rf'\+{var.group(1)}\s*=\s*"([^"]+)"', diff)
            ref = m2.group(1) if m2 else None
    return {
        "name": name, "type": kind, "modalities": modalities,
        "description": description_of(block),
        "reference": ref, "license": field(block, "license"),
        "is_paper": bool(ref and "arxiv" in ref.lower()),
    }


def pr_citation(diff: str) -> str | None:
    m = re.search(r'author\s*=\s*[{"]([^}"]+)[}"].*?year\s*=\s*[{"]?(\d{4})', diff, re.S)
    return apa_cite(m.group(1), m.group(2)) if m else None


def main() -> None:
    rows = []
    for number, label, subdomain in PRS:
        meta = pr_meta(number)
        if meta["state"] != "MERGED":
            sys.exit(f"mteb#{number} is {meta['state']}, not MERGED")
        diff = pr_diff(number)
        imported = imported_names(diff)

        tasks = []
        for m in CLASS_BLOCK_RE.finditer(diff):
            name, kind = m.group(1), m.group(2)
            if name not in imported:
                sys.exit(f"mteb#{number}: {name} defined but never imported — orphaned")
            tasks.append(task_info(name, kind, m.group(0), diff))
        if not tasks:
            sys.exit(f"mteb#{number}: no task classes found")

        modality = "video" if any("video" in t["modalities"] for t in tasks) else "audio"
        if modality == "audio" and not any("audio" in t["modalities"] for t in tasks):
            sys.exit(f"mteb#{number}: no audio or video modality on any task — does not "
                     "belong in this post (see the SEA-VL exclusion note)")

        rows.append({
            "pr": number, "title": meta["title"], "author": meta["author"]["login"],
            "merged": meta["mergedAt"][:10], "label": label, "subdomain": subdomain,
            "modality": modality, "citation": pr_citation(diff), "tasks": tasks,
            "n_tasks": len(tasks),
        })

    total_tasks = sum(r["n_tasks"] for r in rows)
    by_modality: dict[str, int] = {}
    for r in rows:
        by_modality[r["modality"]] = by_modality.get(r["modality"], 0) + r["n_tasks"]
    n_papers = sum(1 for r in rows if any(t["is_paper"] for t in r["tasks"]))

    featured = []
    for subdomain, task_name in FEATURED.items():
        pr_row = next(r for r in rows if r["subdomain"] == subdomain
                      and any(t["name"] == task_name for t in r["tasks"]))
        t = next(t for t in pr_row["tasks"] if t["name"] == task_name)
        featured.append({
            "subdomain": subdomain, "name": t["name"], "dataset": pr_row["label"],
            "description": t["description"], "citation": pr_row["citation"],
            "license": t["license"], "modality": pr_row["modality"],
        })

    evidence = {
        "generated": date.today().isoformat(),
        "source": "gh pr diff, embeddings-benchmark/mteb",
        "excluded": {
            "pr": 5040, "label": "SEA-VL",
            "reason": "modalities are [text, image] on both tasks — no audio, no video; "
                      "does not support this post's claim",
        },
        "n_prs": len(rows), "n_tasks_total": total_tasks,
        "by_modality": by_modality, "n_papers": n_papers,
        "featured": featured,
        "prs": rows,
    }
    (HERE / "data.json").write_text(json.dumps(evidence, indent=2) + "\n")

    write_card_data(HERE / "card.html", {
        "n_prs": len(rows), "n_tasks_total": total_tasks,
        "by_modality": by_modality, "n_papers": n_papers,
        "featured": featured,
    })

    print(f"{len(rows)} PRs, {total_tasks} tasks (audio {by_modality.get('audio', 0)}, "
          f"video {by_modality.get('video', 0)}), {n_papers} of {len(rows)} cite an "
          f"arXiv paper\n")
    for r in rows:
        names = ", ".join(t["name"] for t in r["tasks"])
        print(f"  mteb#{r['pr']:<6} {r['modality']:<6} {r['n_tasks']} task(s)  "
              f"{r['label']} — {r['citation']}")
        print(f"           {names}")
    print("\nfeatured:")
    for f in featured:
        print(f"  [{f['subdomain']}] {f['name']} ({f['dataset']}, {f['citation']})")
        print(f"    {f['description']}")


if __name__ == "__main__":
    main()
