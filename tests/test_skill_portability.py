"""Consumer-installation regression tests for the review Skill pair."""

from __future__ import annotations

import json
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SKILL_NAMES = (
    "code-simplifier",
    "git-commit",
    "review",
    "review-pr",
    "submit-pr",
    "worktree-rebase-merge",
)


FAKE_GH = r'''#!__PYTHON__
import json
import os
import sys

arguments = sys.argv[1:]
url = "https://github.com/owner/repo/pull/42"
identity = {
    "number": 42, "url": url, "headRefOid": "head-1",
    "baseRefName": "main", "baseRefOid": "base-1",
}
full = {
    **identity, "title": "Portable snapshot", "body": "",
    "headRefName": "portable", "headRepository": {"nameWithOwner": "owner/repo"},
    "headRepositoryOwner": {"login": "owner"}, "isCrossRepository": False,
    "isDraft": False, "state": "OPEN", "mergeable": "MERGEABLE",
    "mergeStateStatus": "CLEAN", "updatedAt": "2026-09-11T00:00:00Z",
    "files": [], "commits": [], "closingIssuesReferences": [], "comments": [], "reviews": [],
}
if arguments[:2] == ["pr", "view"]:
    fields = arguments[arguments.index("--json") + 1]
    payload = full if "title" in fields else identity
    if fields == "number,url,headRefOid,baseRefName,baseRefOid" and os.environ.get("FAKE_GH_FINAL_DRIFT") == "1":
        payload = dict(identity, headRefOid="head-2")
    print(json.dumps(payload))
elif arguments[:2] == ["pr", "checks"]:
    print("[]")
elif arguments[:2] == ["repo", "view"]:
    print(json.dumps({
        "nameWithOwner": "acme/project", "defaultBranchRef": {"name": "main"},
        "isFork": False, "parent": None,
    }))
elif arguments[:2] == ["api", "graphql"]:
    query = next(value for value in arguments if value.startswith("query="))
    pr = {"id": "PR_1", "url": url, "headRefOid": "head-1", "state": "OPEN"}
    if "reviewThreads" in query:
        pr["reviewThreads"] = {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}
    print(json.dumps({"data": {"repository": {"pullRequest": pr}}}))
else:
    print("unexpected fake gh arguments: " + repr(arguments), file=sys.stderr)
    sys.exit(2)
'''


class SkillPortabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.consumer = self.root / "consumer"
        self.consumer.mkdir()
        self.skills = self.consumer / "installed-skills"
        ignored = shutil.ignore_patterns("__pycache__")
        for name in PUBLIC_SKILL_NAMES:
            shutil.copytree(REPOSITORY_ROOT / "skills" / name, self.skills / name, ignore=ignored)
        self.standalone_submit = self.root / "standalone-submit-pr" / "submit-pr"
        shutil.copytree(REPOSITORY_ROOT / "skills" / "submit-pr", self.standalone_submit, ignore=ignored)
        self.assertFalse((self.standalone_submit.parent / "git-commit").exists())
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_gh = fake_bin / "gh"
        fake_gh.write_text(FAKE_GH.replace("__PYTHON__", sys.executable), encoding="utf-8")
        fake_gh.chmod(0o755)
        self.environment = dict(
            os.environ,
            PATH=f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            GIT_TERMINAL_PROMPT="0",
            GIT_ASKPASS=os.devnull,
            GIT_ALLOW_PROTOCOL="file",
        )

    def execute(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *arguments], cwd=cwd or self.consumer,
            env=environment or self.environment, text=True, capture_output=True, check=False,
        )

    def review_snapshot(self, *arguments: str, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return self.execute(str(self.skills / "review-pr" / "scripts" / "review_snapshot.py"), *arguments,
                            environment=environment)

    def assert_markdown_links_stay_in_copied_skill_closure(self) -> None:
        closure = self.skills.resolve()
        for markdown in self.skills.rglob("*.md"):
            for match in re.finditer(r"(?<!!)\[[^]]*\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                reference = match.group(1).split(maxsplit=1)[0].strip("<>")
                relative = reference.split("#", maxsplit=1)[0]
                if not relative or "://" in relative or relative.startswith("mailto:"):
                    continue
                target = (markdown.parent / relative).resolve()
                self.assertTrue(target.is_relative_to(closure), f"{markdown}: {reference} escapes copied skills")
                self.assertTrue(target.exists(), f"{markdown}: missing copied target {reference}")

    def git(self, project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *arguments], cwd=project, env=self.environment,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def make_git_project(self) -> Path:
        project = self.consumer / "project"
        project.mkdir()
        self.git(project, "init", "-b", "main")
        self.git(project, "config", "user.name", "Portable Skill Test")
        self.git(project, "config", "user.email", "portable@example.invalid")
        (project / "README.md").write_text("# Portable\n", encoding="utf-8")
        (project / "app.py").write_text("print('base')\n", encoding="utf-8")
        self.git(project, "add", "README.md", "app.py")
        self.git(project, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-m", "chore: seed project")
        base = self.git(project, "rev-parse", "HEAD").stdout.strip()
        self.git(project, "remote", "add", "origin", "https://github.com/acme/project.git")
        self.git(project, "update-ref", "refs/remotes/origin/main", base)
        self.git(project, "checkout", "-b", "feat/portable-helper")
        (project / "app.py").write_text("print('portable')\n", encoding="utf-8")
        self.git(project, "add", "app.py")
        self.git(project, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-m", "feat(cli): run copied helpers")
        return project

    def test_copied_review_skills_collect_refresh_and_reject_drift_without_host_rules(self) -> None:
        """The installed pair operates without source docs or a consumer AGENTS.md."""

        self.assertFalse((self.consumer / "AGENTS.md").exists())
        source_root = str(REPOSITORY_ROOT.resolve())
        for file in self.skills.rglob("*"):
            if file.is_file():
                self.assertNotIn(source_root, file.read_text(encoding="utf-8"))
        self.assert_markdown_links_stay_in_copied_skill_closure()

        initial_path = self.consumer / "initial.json"
        collected = self.review_snapshot(
            "collect", "--repo", "owner/repo", "--pr", "42", "--snapshot-out", str(initial_path),
        )
        self.assertEqual(collected.returncode, 0, collected.stderr)
        initial_page = json.loads(collected.stdout)
        self.assertEqual(initial_page["transport"], "paged")
        self.assertTrue(initial_path.is_file())

        initial = json.loads(initial_path.read_text(encoding="utf-8"))
        snapshot = initial["snapshot"]
        refresh_path = self.consumer / "refresh.json"
        refreshed = self.review_snapshot(
            "refresh", "--repo", "owner/repo", "--pr", "42",
            "--expected-head", snapshot["headRefOid"],
            "--expected-base-name", snapshot["baseRefName"], "--expected-base-sha", snapshot["baseRefOid"],
            "--expected-pr-fingerprint", snapshot["fingerprints"]["pr"],
            "--expected-context-fingerprint", snapshot["fingerprints"]["context"],
            "--expected-threads-fingerprint", snapshot["fingerprints"]["threads"],
            "--expected-checks-fingerprint", snapshot["fingerprints"]["checks"],
            "--previous-snapshot", str(initial_path), "--previous-storage-sha256", initial_page["storage_sha256"],
            "--snapshot-out", str(refresh_path),
        )
        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        stored_refresh = json.loads(refresh_path.read_text(encoding="utf-8"))
        self.assertTrue(stored_refresh["report"]["unchanged"])
        self.assertNotIn("pr", stored_refresh["report"])

        drifting_environment = dict(self.environment, FAKE_GH_FINAL_DRIFT="1")
        collect_drift_path = self.consumer / "collect-drift.json"
        drifted_collect = self.review_snapshot(
            "collect", "--repo", "owner/repo", "--pr", "42", "--snapshot-out", str(collect_drift_path),
            environment=drifting_environment,
        )
        self.assertEqual(drifted_collect.returncode, 1)
        self.assertIn("identity changed after parallel collection", drifted_collect.stderr)
        self.assertFalse(collect_drift_path.exists(), "failed collection must not save a new snapshot")

        refresh_drift_path = self.consumer / "refresh-drift.json"
        drifted = self.review_snapshot(
            "refresh", "--repo", "owner/repo", "--pr", "42",
            "--expected-head", snapshot["headRefOid"],
            "--expected-pr-fingerprint", snapshot["fingerprints"]["pr"],
            "--expected-context-fingerprint", snapshot["fingerprints"]["context"],
            "--expected-threads-fingerprint", snapshot["fingerprints"]["threads"],
            "--expected-checks-fingerprint", snapshot["fingerprints"]["checks"],
            "--snapshot-out", str(refresh_drift_path),
            environment=drifting_environment,
        )
        self.assertEqual(drifted.returncode, 1)
        self.assertIn("identity changed after parallel collection", drifted.stderr)
        self.assertFalse(refresh_drift_path.exists(), "failed refresh must not save a new snapshot")

        agents = self.consumer / "AGENTS.md"
        self.assertFalse(agents.exists(), "helpers must not create consumer rules")
        agents_text = "No commits, ref updates, or project-rule edits.\n"
        agents.write_text(agents_text, encoding="utf-8")
        under_rules = self.review_snapshot("collect", "--repo", "owner/repo", "--pr", "42")
        self.assertEqual(under_rules.returncode, 0, under_rules.stderr)
        self.assertEqual(agents.read_text(encoding="utf-8"), agents_text)
        self.assertFalse((self.consumer / "docs").exists())

    def test_all_copied_skills_run_git_helpers_without_host_rules_or_git_mutation(self) -> None:
        """Copied Git helpers use only their installation and a supplied local repository."""

        self.assertFalse((self.consumer / "AGENTS.md").exists())
        self.assert_markdown_links_stay_in_copied_skill_closure()
        project = self.make_git_project()
        refs_before = self.git(project, "show-ref").stdout
        index_before = (project / ".git" / "index").read_bytes()
        status_before = self.git(project, "status", "--porcelain=v1").stdout
        message = self.consumer / "message.txt"
        message.write_text(
            "feat(cli): validate copied helper\n\n"
            "Explain the portable test context.\n\n"
            "Run the copied helper scripts.\n\n"
            "Keep the consumer repository unchanged.\n",
            encoding="utf-8",
        )

        validator = self.execute(
            str(self.skills / "git-commit" / "scripts" / "validate-commit-message.py"),
            "--file", str(message), "--mode", "english",
            environment=self.environment,
        )
        self.assertEqual(validator.returncode, 0, validator.stderr)
        self.assertNotIn(str(REPOSITORY_ROOT), str(validator.args))
        stats = self.execute(
            str(self.skills / "git-commit" / "scripts" / "commit-change-stats.py"), "HEAD",
            environment=self.environment, cwd=project,
        )
        self.assertEqual(stats.returncode, 0, stats.stderr)
        self.assertEqual(json.loads(stats.stdout)["scope"], "commit")
        facts = self.execute(
            str(self.skills / "worktree-rebase-merge" / "scripts" / "collect-integration-facts.py"),
            "--source", str(project), "--target", "main",
            environment=self.environment, cwd=project,
        )
        self.assertEqual(facts.returncode, 0, facts.stderr)
        facts_payload = json.loads(facts.stdout)
        self.assertTrue(facts_payload["stable"])
        self.assertEqual(facts_payload["target"]["name"], "main")
        self.assertEqual(self.git(project, "show-ref").stdout, refs_before)
        self.assertEqual((project / ".git" / "index").read_bytes(), index_before)
        self.assertEqual(self.git(project, "status", "--porcelain=v1").stdout, status_before)
        submit_plan = self.execute(
            str(self.standalone_submit / "scripts" / "submit_pr.py"), "plan",
            "--repo-root", str(project),
            "--title", "feat(cli): run copied helpers",
            "--summary", "Exercise copied helper assets.",
            "--verification", "- Portable helper subprocesses passed.",
            environment=self.environment, cwd=project,
        )
        self.assertEqual(submit_plan.returncode, 0, submit_plan.stderr)
        self.assertEqual(json.loads(submit_plan.stdout)["mode"], "plan")
        self.assertNotIn(str(REPOSITORY_ROOT), str(submit_plan.args))
        self.assertFalse((project / "AGENTS.md").exists())
        self.assertEqual(self.git(project, "show-ref").stdout, refs_before)
        self.assertEqual((project / ".git" / "index").read_bytes(), index_before)
        self.assertEqual(self.git(project, "status", "--porcelain=v1").stdout, status_before)

        agents = project / "AGENTS.md"
        agents_text = "Do not commit, update refs, or edit project rules.\n"
        agents.write_text(agents_text, encoding="utf-8")
        refs_under_rules = self.git(project, "show-ref").stdout
        index_under_rules = (project / ".git" / "index").read_bytes()
        status_under_rules = self.git(project, "status", "--porcelain=v1").stdout
        under_rules = self.execute(
            str(self.skills / "submit-pr" / "scripts" / "submit_pr.py"), "plan",
            "--repo-root", str(project),
            "--title", "feat(cli): run copied helpers",
            "--summary", "Exercise copied helper assets.",
            "--verification", "- Portable helper subprocesses passed.",
            environment=self.environment, cwd=project,
        )
        self.assertEqual(under_rules.returncode, 0, under_rules.stderr)
        self.assertEqual(agents.read_text(encoding="utf-8"), agents_text)
        self.assertEqual(self.git(project, "show-ref").stdout, refs_under_rules)
        self.assertEqual((project / ".git" / "index").read_bytes(), index_under_rules)
        self.assertEqual(self.git(project, "status", "--porcelain=v1").stdout, status_under_rules)
        self.assertFalse((self.consumer / "docs").exists())
        self.assertFalse((project / "docs").exists())

    def test_copied_local_review_helper_preserves_consumer_rules_index_and_refs(self) -> None:
        """The local helper can inspect a consumer Git repository without mutating it."""

        agents = self.consumer / "AGENTS.md"
        agents.write_text("Do not create commits or modify Git refs.\n", encoding="utf-8")
        (self.consumer / "example.txt").write_text("first\n", encoding="utf-8")
        for command in (("git", "init"), ("git", "add", "example.txt"),
                        ("git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "initial")):
            result = subprocess.run(command, cwd=self.consumer, text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)

        index_before = (self.consumer / ".git" / "index").read_bytes()
        refs_before = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname):%(objectname)"], cwd=self.consumer,
            text=True, capture_output=True, check=False,
        ).stdout
        status_before = subprocess.run(["git", "status", "--porcelain=v1"], cwd=self.consumer,
                                       text=True, capture_output=True, check=False).stdout

        result = self.execute(
            str(self.skills / "review" / "scripts" / "collect_review_snapshot.py"),
            "--repo", str(self.consumer), "--commit", "HEAD",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["state"], "collected")
        self.assertEqual(agents.read_text(encoding="utf-8"), "Do not create commits or modify Git refs.\n")
        self.assertEqual((self.consumer / ".git" / "index").read_bytes(), index_before)
        refs_after = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname):%(objectname)"], cwd=self.consumer,
            text=True, capture_output=True, check=False,
        ).stdout
        status_after = subprocess.run(["git", "status", "--porcelain=v1"], cwd=self.consumer,
                                      text=True, capture_output=True, check=False).stdout
        self.assertEqual(refs_after, refs_before)
        self.assertEqual(status_after, status_before)


if __name__ == "__main__":
    unittest.main()
