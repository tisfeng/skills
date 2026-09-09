#!/usr/bin/env python3
"""Collect and verify read-only Git integration checkpoints as JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


class InspectionError(RuntimeError):
    """Git evidence could not be collected safely."""


def git(repo: str, *args: str, allowed: tuple[int, ...] = (0,)) -> str:
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", LC_ALL="C")
    try:
        result = subprocess.run(
            ["git", "--no-pager", "-c", "core.fsmonitor=false", "-C", repo, *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise InspectionError(f"Cannot inspect {repo}: {error}") from error
    if result.returncode not in allowed:
        detail = os.fsdecode(result.stderr).strip()
        raise InspectionError(f"git {args[0]} in {repo}: {detail or result.returncode}")
    return os.fsdecode(result.stdout)


def branch_ref(repo: str, name: str) -> str:
    ref = f"refs/heads/{name}"
    git(repo, "check-ref-format", ref)
    return ref


def oid(repo: str, ref: str) -> str:
    return git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").strip()


def worktrees(repo: str) -> list[dict[str, str]]:
    records = []
    for block in git(repo, "worktree", "list", "--porcelain", "-z").split("\0\0"):
        if not block:
            continue
        record = {}
        for field in block.split("\0"):
            if field:
                key, _, value = field.partition(" ")
                record[key] = value
        records.append(record)
    return records


def checkout(path: str) -> dict:
    root = git(path, "rev-parse", "--show-toplevel").removesuffix("\n")
    git_dir = git(path, "rev-parse", "--absolute-git-dir").removesuffix("\n")
    common = git(path, "rev-parse", "--path-format=absolute", "--git-common-dir").removesuffix("\n")
    operations = [
        name for name in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD",
                          "rebase-merge", "rebase-apply", "sequencer", "BISECT_START")
        if (Path(git_dir) / name).exists()
    ]
    status = git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all",
                 "--ignore-submodules=none")
    return {
        "path": str(Path(root).resolve()), "git_dir": git_dir, "common_dir": common,
        "head": oid(path, "HEAD"),
        "branch": git(path, "symbolic-ref", "-q", "HEAD", allowed=(0, 1)).strip() or None,
        "status": status, "operations": operations,
        "index_sha256": hashlib.sha256(os.fsencode(git(path, "ls-files", "--stage", "-v", "-z"))).hexdigest(),
        "clean": not status and not operations,
    }


def resolve_target(repo: str, target: str | None) -> tuple[str, dict]:
    if target:
        branch_ref(repo, target)
        return target, {"kind": "explicit"}
    remotes = git(repo, "remote").splitlines()
    remote = "origin" if "origin" in remotes else remotes[0] if len(remotes) == 1 else None
    if remote is None:
        raise InspectionError("Specify --target: remote selection is ambiguous or unavailable")
    try:
        output = git(repo, "ls-remote", "--symref", "--", remote, "HEAD")
        for line in output.splitlines():
            if line.startswith("ref: refs/heads/") and line.endswith("\tHEAD"):
                name = line[len("ref: refs/heads/"):-len("\tHEAD")]
                branch_ref(repo, name)
                return name, {"kind": "remote-head", "remote": remote}
    except InspectionError as error:
        detail = str(error)
    else:
        detail = "remote HEAD does not name a branch"
    candidate = git(repo, "symbolic-ref", "-q", f"refs/remotes/{remote}/HEAD",
                    allowed=(0, 1)).strip()
    raise InspectionError(
        f"Specify or confirm --target: {detail}; cached candidate (not selected): {candidate or 'none'}"
    )


def select_branch(repo: str, requested: str | None, source: dict, occupancy: list[dict]) -> dict | None:
    if source["branch"] or requested is None:
        return None
    branch_ref(repo, requested)
    refs = {}
    for line in git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/").splitlines():
        ref, head = line.split(" ", 1)
        refs[ref] = head
    occupied = {item.get("branch") for item in occupancy}
    number = 1
    while True:
        name = requested if number == 1 else f"{requested}-{number}"
        ref = branch_ref(repo, name)
        if ref not in refs:
            return {"name": name, "action": "create"}
        if refs[ref] == source["head"] and ref not in occupied:
            return {"name": name, "action": "reuse"}
        number += 1


def collect(source_path: str, target: str, requested_branch: str | None) -> tuple[dict, list[str]]:
    source = checkout(source_path)
    repo = source["path"]
    target_ref = branch_ref(repo, target)
    target_head = oid(repo, target_ref)
    occupancy = worktrees(repo)
    targets = [checkout(item["worktree"]) for item in occupancy if item.get("branch") == target_ref]
    selected = next((item["path"] for item in targets if item["clean"]), None)
    blockers = []
    if not source["clean"]:
        blockers.append("source-not-clean")
    if targets and selected is None:
        blockers.append("target-not-clean")
    if source["branch"] == target_ref:
        blockers.append("same-branch-direct-commit")
    if any(item["branch"] != target_ref or item["head"] != target_head
           or item["common_dir"] != source["common_dir"] for item in targets):
        blockers.append("target-checkout-mismatch")
    revision_range = f"{target_head}..{source['head']}"
    commits = git(repo, "rev-list", "--reverse", revision_range, "--").splitlines()
    if not commits:
        blockers.append("no-source-commits")
    bases = git(repo, "merge-base", "--all", target_head, source["head"], allowed=(0, 1)).splitlines()
    if len(bases) != 1:
        blockers.append("ambiguous-or-missing-merge-base")
    # Include every commit's touched paths, including changes later reverted.
    paths = sorted(set(filter(None, git(
        repo, "log", "--format=", "--name-only", "-z", "--no-renames", "-m",
        "--no-ext-diff", "--no-textconv", revision_range, "--",
    ).split("\0"))))
    state = {
        "source": source,
        "target": {"ref": target_ref, "head": target_head, "checkouts": targets, "selected": selected,
                   "mode": "existing-target-worktree" if targets else "temporary-target-worktree"},
        "worktrees": occupancy,
        "source_branch": select_branch(repo, requested_branch, source, occupancy),
        "range": {"commits": commits, "paths": paths, "merge_bases": bases},
    }
    # Reject drift observed within collection; this is not a lock across commands.
    if (checkout(repo) != source or oid(repo, target_ref) != target_head
            or worktrees(repo) != occupancy or [checkout(item["path"]) for item in targets] != targets):
        blockers.append("state-changed-during-inspection")
    return state, blockers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot", help="Print a read-only checkpoint")
    snapshot.add_argument("--source", default=".")
    snapshot.add_argument("--target", help="Local target branch; otherwise query live remote HEAD")
    snapshot.add_argument("--source-branch", help="Candidate name when the source is detached")
    verify = commands.add_parser("verify", help="Compare current state with a checkpoint")
    verify.add_argument("--snapshot", required=True, help="JSON file, or - for stdin")
    args = parser.parse_args()
    try:
        expected = None
        if args.command == "verify":
            raw = sys.stdin.read() if args.snapshot == "-" else Path(args.snapshot).read_text()
            expected = json.loads(raw)
            if expected.get("schema_version") != 1 or expected.get("blockers"):
                raise InspectionError("Expected a version 1 checkpoint without blockers; inspect again")
            request = expected["request"]
            resolution = expected["target_resolution"]
        else:
            target, resolution = resolve_target(args.source, args.target)
            request = {"source": str(Path(args.source).resolve()), "target": target,
                       "source_branch": args.source_branch}
        state, blockers = collect(request["source"], request["target"], request["source_branch"])
        changed = [] if expected is None else [key for key in state if state[key] != expected["state"].get(key)]
        if changed:
            blockers.append("checkpoint-drift")
        payload = {"schema_version": 1, "request": request, "target_resolution": resolution,
                   "state": state, "blockers": blockers, "changed_fields": changed}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 2 if blockers else 0
    except (InspectionError, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(json.dumps({"error": str(error), "action": "Inspect the reported state before retrying"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
