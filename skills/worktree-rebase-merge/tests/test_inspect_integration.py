from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "inspect-integration.py"
SPEC = importlib.util.spec_from_file_location("inspect_integration", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
inspect_integration = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inspect_integration
SPEC.loader.exec_module(inspect_integration)


def run_git(path: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode:
        raise AssertionError(
            f"git command failed: {args!r}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class InspectIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        hooks = self.root / "empty-hooks"
        hooks.mkdir()
        run_git(self.root, "init", "-b", "main", str(self.repo))
        run_git(self.repo, "config", "user.name", "Integration Test")
        run_git(self.repo, "config", "user.email", "integration@example.com")
        run_git(self.repo, "config", "commit.gpgsign", "false")
        run_git(self.repo, "config", "core.hooksPath", str(hooks))
        self.write("base.txt", "base\n")
        self.write("old.txt", "old\n")
        self.write("shared.txt", "base\n")
        self.write("odd\nname.txt", "initial\n")
        self.commit("chore: seed repository")
        run_git(self.repo, "switch", "-c", "feature")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, name: str, content: str, *, path: Path | None = None) -> Path:
        destination = (path or self.repo) / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return destination

    def commit(self, message: str, *, path: Path | None = None) -> str:
        repository = path or self.repo
        run_git(repository, "add", "-A")
        run_git(repository, "-c", "commit.gpgsign=false", "commit", "-m", message)
        return run_git(repository, "rev-parse", "HEAD").stdout.strip()

    def commit_feature(self, name: str = "feature.txt", content: str = "feature\n") -> str:
        self.write(name, content)
        return self.commit("feat: add feature evidence")

    def add_target_worktree(self, name: str = "target") -> Path:
        target = self.root / name
        run_git(self.repo, "worktree", "add", str(target), "main")
        return target

    def command(self, *args: str, input: str | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            cwd=self.root,
            input=input,
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise AssertionError(
                f"script did not emit JSON\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            ) from error
        return result, payload

    def snapshot(self, *, target: str = "main", source_branch: str | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
        arguments = ["snapshot", "--source", str(self.repo), "--target", target]
        if source_branch is not None:
            arguments.extend(["--source-branch", source_branch])
        return self.command(*arguments)

    def save_snapshot(self, payload: dict, name: str = "checkpoint.json") -> Path:
        snapshot = self.root / name
        snapshot.write_text(json.dumps(payload), encoding="utf-8")
        return snapshot

    def verify(self, snapshot: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
        return self.command("verify", "--snapshot", str(snapshot))

    def assert_snapshot_ok(self, result: subprocess.CompletedProcess[str], payload: dict) -> None:
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["blockers"], [])
        self.assertEqual(payload["changed_fields"], [])

    def test_clean_snapshot_is_read_only_and_normal_rebase_merge_leaves_no_range(self) -> None:
        source_commit = self.commit_feature()
        target = self.add_target_worktree()
        self.write("target.txt", "target\n", path=target)
        self.commit("chore: advance target", path=target)

        git_dir = Path(run_git(self.repo, "rev-parse", "--absolute-git-dir").stdout.strip())
        index = Path(run_git(self.repo, "rev-parse", "--git-path", "index").stdout.strip())
        before = {
            "head": (git_dir / "HEAD").read_bytes(),
            "index": index.read_bytes(),
            "refs": run_git(self.repo, "show-ref", "--head").stdout,
            "worktrees": run_git(self.repo, "worktree", "list", "--porcelain").stdout,
            "source_status": run_git(self.repo, "status", "--porcelain=v1", "-z").stdout,
            "target_status": run_git(target, "status", "--porcelain=v1", "-z").stdout,
        }

        result, payload = self.snapshot()

        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["target_resolution"], {"kind": "explicit"})
        self.assertEqual(payload["state"]["range"]["commits"], [source_commit])
        self.assertEqual(payload["state"]["target"]["mode"], "existing-target-worktree")
        self.assertEqual(payload["state"]["target"]["selected"], str(target.resolve()))
        self.assertEqual((git_dir / "HEAD").read_bytes(), before["head"])
        self.assertEqual(index.read_bytes(), before["index"])
        self.assertEqual(run_git(self.repo, "show-ref", "--head").stdout, before["refs"])
        self.assertEqual(run_git(self.repo, "worktree", "list", "--porcelain").stdout, before["worktrees"])
        self.assertEqual(run_git(self.repo, "status", "--porcelain=v1", "-z").stdout, before["source_status"])
        self.assertEqual(run_git(target, "status", "--porcelain=v1", "-z").stdout, before["target_status"])

        run_git(self.repo, "rebase", "main")
        run_git(target, "merge", "feature")
        self.assertTrue(
            run_git(target, "merge-base", "--is-ancestor", "feature", "main").returncode == 0
        )

        result, payload = self.snapshot()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["blockers"], ["no-source-commits"])
        self.assertEqual(payload["state"]["range"]["commits"], [])

    def test_source_and_target_dirty_states_include_untracked_files(self) -> None:
        self.commit_feature()
        target = self.add_target_worktree()
        self.write("source-untracked.txt", "source\n")

        result, payload = self.snapshot()
        self.assertEqual(result.returncode, 2)
        self.assertIn("source-not-clean", payload["blockers"])
        self.assertIn("?? source-untracked.txt", payload["state"]["source"]["status"])

        (self.repo / "source-untracked.txt").unlink()
        self.write("target-untracked.txt", "target\n", path=target)
        self.write("target-dirty.txt", "dirty\n", path=target)
        result, payload = self.snapshot()
        self.assertEqual(result.returncode, 2)
        self.assertIn("target-not-clean", payload["blockers"])
        target_state = payload["state"]["target"]["checkouts"][0]
        self.assertIn("?? target-untracked.txt", target_state["status"])
        self.assertIn("?? target-dirty.txt", target_state["status"])

    def test_verify_detects_source_target_and_target_occupancy_drift(self) -> None:
        self.commit_feature()
        result, payload = self.snapshot()
        self.assert_snapshot_ok(result, payload)
        checkpoint = self.save_snapshot(payload, "source.json")

        self.commit_feature("later.txt", "later\n")
        result, payload = self.verify(checkpoint)
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkpoint-drift", payload["blockers"])
        self.assertIn("source", payload["changed_fields"])
        self.assertIn("range", payload["changed_fields"])

        target = self.add_target_worktree()
        result, payload = self.snapshot()
        self.assert_snapshot_ok(result, payload)
        checkpoint = self.save_snapshot(payload, "target.json")
        self.write("target-advance.txt", "target\n", path=target)
        self.commit("chore: advance target", path=target)
        result, payload = self.verify(checkpoint)
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkpoint-drift", payload["blockers"])
        self.assertIn("target", payload["changed_fields"])

        run_git(self.repo, "worktree", "remove", str(target))
        result, payload = self.snapshot()
        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["state"]["target"]["mode"], "temporary-target-worktree")
        checkpoint = self.save_snapshot(payload, "occupancy.json")
        self.add_target_worktree()
        result, payload = self.verify(checkpoint)
        self.assertEqual(result.returncode, 2)
        self.assertIn("target", payload["changed_fields"])
        self.assertIn("worktrees", payload["changed_fields"])

    def test_same_branch_is_blocked_even_when_head_oid_matches_target(self) -> None:
        run_git(self.repo, "switch", "main")

        result, payload = self.snapshot()

        self.assertEqual(result.returncode, 2)
        self.assertIn("same-branch-direct-commit", payload["blockers"])
        self.assertIn("no-source-commits", payload["blockers"])

    def test_detached_source_reuses_matching_branch_or_selects_conflict_suffix_when_occupied(self) -> None:
        source_commit = self.commit_feature()
        target = self.add_target_worktree()
        run_git(self.repo, "checkout", "--detach", source_commit)

        result, payload = self.snapshot(source_branch="feature")
        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["state"]["source_branch"], {"name": "feature", "action": "reuse"})

        occupied = self.root / "occupied-feature"
        run_git(self.repo, "worktree", "add", str(occupied), "feature")
        result, payload = self.snapshot(source_branch="feature")
        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["state"]["target"]["selected"], str(target.resolve()))
        self.assertEqual(payload["state"]["source_branch"], {"name": "feature-2", "action": "create"})

    def test_temporary_target_mode_and_complete_path_history_include_reverted_renamed_and_newline_names(self) -> None:
        first = self.commit_feature("reverted.txt", "will be removed\n")
        (self.repo / "reverted.txt").unlink()
        second = self.commit("fix: remove intermediate file")
        run_git(self.repo, "mv", "old.txt", "renamed.txt")
        third = self.commit("refactor: rename evidence file")
        self.write("odd\nname.txt", "changed\n")
        fourth = self.commit("fix: change newline file name")

        result, payload = self.snapshot()

        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["state"]["target"]["mode"], "temporary-target-worktree")
        self.assertIsNone(payload["state"]["target"]["selected"])
        self.assertEqual(payload["state"]["range"]["commits"], [first, second, third, fourth])
        self.assertEqual(
            payload["state"]["range"]["paths"],
            sorted(["old.txt", "odd\nname.txt", "renamed.txt", "reverted.txt"]),
        )

    def test_merge_conflict_is_a_source_blocker_and_records_operation(self) -> None:
        self.write("shared.txt", "feature\n")
        self.commit("feat: edit shared file")
        target = self.add_target_worktree()
        self.write("shared.txt", "main\n", path=target)
        self.commit("fix: edit shared file", path=target)
        merge = run_git(self.repo, "merge", "main", check=False)
        self.assertNotEqual(merge.returncode, 0)

        result, payload = self.snapshot()

        self.assertEqual(result.returncode, 2)
        self.assertIn("source-not-clean", payload["blockers"])
        self.assertIn("MERGE_HEAD", payload["state"]["source"]["operations"])
        self.assertIn("UU shared.txt", payload["state"]["source"]["status"])

    def test_verify_permission_error_is_a_read_failure_without_sandbox_claim(self) -> None:
        stream = io.StringIO()
        with (
            patch.object(inspect_integration.Path, "read_text", side_effect=PermissionError("permission denied")),
            patch.object(sys, "argv", [str(SCRIPT_PATH), "verify", "--snapshot", "checkpoint.json"]),
            contextlib.redirect_stdout(stream),
        ):
            exit_code = inspect_integration.main()

        payload = json.loads(stream.getvalue())
        self.assertEqual(exit_code, 1)
        self.assertIn("permission denied", payload["error"])
        self.assertNotIn("sandbox", payload["error"].lower())

    def test_default_remote_head_is_live_and_failed_query_does_not_select_cached_head(self) -> None:
        remote = self.root / "remote.git"
        run_git(self.root, "init", "--bare", "--initial-branch=main", str(remote))
        run_git(self.repo, "remote", "add", "origin", str(remote))
        run_git(self.repo, "push", "origin", "main")
        self.commit_feature()

        result, payload = self.command("snapshot", "--source", str(self.repo))
        self.assert_snapshot_ok(result, payload)
        self.assertEqual(payload["request"]["target"], "main")
        self.assertEqual(payload["target_resolution"], {"kind": "remote-head", "remote": "origin"})

        run_git(self.repo, "remote", "set-url", "origin", str(self.root / "missing-remote.git"))
        run_git(self.repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        result, payload = self.command("snapshot", "--source", str(self.repo))
        self.assertEqual(result.returncode, 1)
        self.assertIn("cached candidate (not selected): refs/remotes/origin/main", payload["error"])
        self.assertNotIn("target_resolution", payload)


if __name__ == "__main__":
    unittest.main()
