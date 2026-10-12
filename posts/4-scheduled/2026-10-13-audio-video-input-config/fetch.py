#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["mteb==2.24.10", "packaging"]
#
# [tool.uv]
# exclude-newer = "2026-10-13T00:00:00Z"
# ///
"""Evidence for the audio/video input-config post (mteb#5454). Run from the repo root:

    uv run posts/4-scheduled/2026-10-13-audio-video-input-config/fetch.py

No score is published in this post, so nothing here goes through `get_score()`. The post
makes two countable claims, and both are computed rather than taken from the PR:

1. **How many model wrappers changed behaviour.** The PR touches 66 files under
   `mteb/models`, but a third of them only gained a source comment. Each changed file is
   parsed at the parent and at the merge commit, and counts as a behavioural change only
   if its AST differs once docstrings are removed (comments never reach the AST).
2. **How many models have audio or video results that predate the change.** Every
   result file in the results repo carries the `mteb_version` that produced it. A model
   counts if it has at least one result on a task whose `modalities` include audio or
   video, computed with mteb < 2.24.4 — the first release containing the merge commit
   (checked: `compare/2.24.3...<sha>` is "ahead", `compare/2.24.4...<sha>` is "behind").

What this deliberately does *not* claim: that every one of those models' scores moves.
The shared frame sampler (`FramesCollator.resample_video`) changed for every video path in
mteb, and audio caps changed per wrapper, but whether a given score moves depends on the
clip lengths in each task. MTEB's own release note says results from earlier versions
"are not comparable", which is the claim the post repeats — not a per-model one.
"""

import ast
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request
import warnings
from collections import Counter
from datetime import date

warnings.filterwarnings("ignore")

from packaging.version import InvalidVersion, Version  # noqa: E402

REPO = "embeddings-benchmark/mteb"
MERGE_SHA = "5621901c07940b64ff71cd00e74b20f362571eeb"
FIRST_RELEASE = Version("2.24.4")
HERE = pathlib.Path(__file__).parent
CACHE = pathlib.Path.home() / ".cache" / "mteb" / "remote"


def gh_json(path: str):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def raw(sha: str, path: str) -> str | None:
    url = f"https://raw.githubusercontent.com/{REPO}/{sha}/{path}"
    try:
        with urllib.request.urlopen(url) as r:
            return r.read().decode()
    except urllib.error.HTTPError:
        return None


def normalised_ast(src: str) -> str:
    """AST dump with docstrings removed, so a comment- or docstring-only edit compares equal."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (
            isinstance(body, list)
            and body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            node.body = body[1:] or [ast.Pass()]  # type: ignore[attr-defined]
    return ast.dump(tree, include_attributes=False)


def changed_modules() -> tuple[list[str], list[str]]:
    commit = gh_json(f"repos/{REPO}/commits/{MERGE_SHA}")
    parent = commit["parents"][0]["sha"]
    behavioural, comment_only = [], []
    for f in commit["files"]:
        p = f["filename"]
        if not (p.startswith("mteb/models/") and p.endswith(".py")):
            continue
        before, after = raw(parent, p), raw(MERGE_SHA, p)
        if before is None or after is None or normalised_ast(before) != normalised_ast(after):
            behavioural.append(p)
        else:
            comment_only.append(p)
    return sorted(behavioural), sorted(comment_only)


def update_results_cache() -> str:
    subprocess.run(["git", "-C", str(CACHE), "pull", "--ff-only", "-q"], check=True)
    return subprocess.run(
        ["git", "-C", str(CACHE), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def main() -> None:
    print("diffing changed modules ...", flush=True)
    behavioural, comment_only = changed_modules()
    wrappers = [p for p in behavioural if "/model_implementations/" in p]
    print(f"  {len(behavioural)} behavioural ({len(wrappers)} wrappers), {len(comment_only)} comment-only", flush=True)

    print("updating results cache ...", flush=True)
    results_sha = update_results_cache()

    print("importing mteb (~3 min) ...", flush=True)
    import mteb

    modality_cache: dict[str, list[str] | None] = {}

    def modalities(task_name: str) -> list[str] | None:
        if task_name not in modality_cache:
            try:
                modality_cache[task_name] = list(mteb.get_task(task_name).metadata.modalities)
            except Exception:
                modality_cache[task_name] = None  # task no longer in the registry
        return modality_cache[task_name]

    models: dict[str, dict] = {}
    unknown_tasks: Counter = Counter()
    for f in sorted((CACHE / "results").glob("*/*/*.json")):
        if f.name == "model_meta.json":
            continue
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        task = d.get("task_name") or f.stem
        mods = modalities(task)
        if mods is None:
            unknown_tasks[task] += 1
            continue
        av = sorted(set(mods) & {"audio", "video"})
        if not av:
            continue
        model = f.parent.parent.name.replace("__", "/", 1)
        try:
            v = Version(str(d.get("mteb_version")))
        except InvalidVersion:
            v = None
        m = models.setdefault(model, {"audio": 0, "video": 0, "pre": 0, "post": 0, "unknown_version": 0, "versions": set()})
        for x in av:
            m[x] += 1
        if v is None:
            m["unknown_version"] += 1
        elif v < FIRST_RELEASE:
            m["pre"] += 1
        else:
            m["post"] += 1
        m["versions"].add(str(v))

    # Why the old 30 s cap mattered: how many audio tasks contain clips longer than it.
    # Read from the task's own descriptive statistics shipped with mteb. Conservative
    # count = evaluation splits only; the any-split count also includes the train splits
    # that classification tasks embed to fit their probe (BirdSet: test clips are 5 s,
    # train clips run to 1,190 s), which the cap truncated just the same.
    stats_root = pathlib.Path(mteb.__file__).parent / "descriptive_stats"
    long_eval, long_any, n_audio_tasks = [], [], 0
    for task in mteb.get_tasks(modalities=["audio"]):
        files = list(stats_root.glob(f"*/{task.metadata.name}.json"))
        if not files:
            continue
        n_audio_tasks += 1
        stats = json.loads(files[0].read_text())
        def split_max(split_stats) -> float:
            a = (split_stats or {}).get("audio_statistics") or {}
            return float(a.get("max_duration_seconds") or 0)
        eval_max = max((split_max(stats.get(s)) for s in task.metadata.eval_splits), default=0)
        any_max = max((split_max(v) for v in stats.values() if isinstance(v, dict)), default=0)
        if eval_max > 30:
            long_eval.append((task.metadata.name, round(eval_max, 1)))
        if any_max > 30:
            long_any.append((task.metadata.name, round(any_max, 1)))

    with_av = sorted(models)
    pre = [k for k in with_av if models[k]["pre"] > 0]
    any_post = [k for k in with_av if models[k]["post"] > 0]
    only_post = [k for k in with_av if models[k]["pre"] == 0 and models[k]["unknown_version"] == 0]

    summary = {
        "models_with_audio_or_video_results": len(with_av),
        "of_which_any_result_before_2_24_4": len(pre),
        "of_which_any_result_on_or_after_2_24_4": len(any_post),
        "of_which_all_results_on_or_after_2_24_4": len(only_post),
        "models_with_audio_results": sum(1 for k in with_av if models[k]["audio"]),
        "models_with_video_results": sum(1 for k in with_av if models[k]["video"]),
        "behavioural_wrapper_modules": len(wrappers),
        "comment_only_modules": len(comment_only),
        "audio_tasks_with_stats": n_audio_tasks,
        "audio_tasks_with_clips_over_30s_in_eval_splits": len(long_eval),
        "audio_tasks_with_clips_over_30s_in_any_split": len(long_any),
    }
    print(json.dumps(summary, indent=2))

    (HERE / "data.json").write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "mteb_merge_commit": MERGE_SHA,
                "first_release": str(FIRST_RELEASE),
                "results_repo_commit": results_sha,
                "summary": summary,
                "behavioural_modules": behavioural,
                "comment_only_modules": comment_only,
                "audio_tasks_over_30s_eval_splits": sorted(long_eval, key=lambda x: -x[1]),
                "audio_tasks_over_30s_any_split": sorted(long_any, key=lambda x: -x[1]),
                "models": {k: {**v, "versions": sorted(v["versions"])} for k, v in sorted(models.items())},
                "result_files_on_unregistered_tasks": dict(unknown_tasks.most_common()),
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    sys.exit(main())
