"""Behavior tests for repository-local Skill discovery validation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate-skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills_under_test", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
validate_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skills)


class ValidateDiscoveryEntriesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repository_root = Path(self.temporary_directory.name)
        self.skills_root = self.repository_root / "skills"
        self.discovery_root = self.repository_root / ".agents" / "skills"
        self.skills_root.mkdir()
        self.discovery_root.mkdir(parents=True)
        self.repository_root_patch = patch.object(
            validate_skills, "REPOSITORY_ROOT", self.repository_root
        )
        self.repository_root_patch.start()
        self.addCleanup(self.repository_root_patch.stop)
        self.add_internal_release()

    def add_published_skill(self, name: str, *, entrypoint: bool = True) -> Path:
        skill_directory = self.skills_root / name
        skill_directory.mkdir()
        if entrypoint:
            (skill_directory / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
        return skill_directory

    def add_discovery_link(self, name: str, target: Path | None = None) -> Path:
        entry = self.discovery_root / name
        entry.symlink_to(target or Path("../../skills") / name, target_is_directory=True)
        return entry

    def add_internal_release(self) -> None:
        release = self.discovery_root / "release"
        release.mkdir()
        (release / "SKILL.md").write_text(
            "---\nname: release\ndescription: Internal release workflow\n---\n",
            encoding="utf-8",
        )

    def validate(self, *skill_directories: Path) -> list[str]:
        return validate_skills.validate_discovery_entries(skill_directories)

    def test_accepts_multiple_relative_public_links_and_real_internal_release(self) -> None:
        git_commit = self.add_published_skill("git-commit")
        review = self.add_published_skill("review")
        self.add_discovery_link("git-commit")
        self.add_discovery_link("review")

        self.assertEqual(self.validate(git_commit, review), [])

    def test_reports_missing_public_discovery_entry(self) -> None:
        skill = self.add_published_skill("review")

        self.assertEqual(
            self.validate(skill),
            [".agents/skills/review: create a relative symlink to ../../skills/review"],
        )

    def test_reports_copied_public_skill_instead_of_link(self) -> None:
        skill = self.add_published_skill("review")
        copied_entry = self.discovery_root / "review"
        copied_entry.mkdir()
        (copied_entry / "SKILL.md").write_text("# Copied\n", encoding="utf-8")

        self.assertEqual(
            self.validate(skill),
            [".agents/skills/review: create a relative symlink to ../../skills/review"],
        )

    def test_reports_absolute_or_wrong_public_link_targets(self) -> None:
        for name, target in (
            ("absolute-target", Path("/outside-the-repository/absolute-target")),
            ("wrong-target", Path("../../skills/another-skill")),
        ):
            with self.subTest(target=target):
                skill = self.add_published_skill(name)
                self.add_discovery_link(name, target)

                self.assertEqual(
                    self.validate(skill),
                    [
                        f".agents/skills/{name}: symlink must target "
                        f"../../skills/{name}"
                    ],
                )
                (self.discovery_root / name).unlink()
                (skill / "SKILL.md").unlink()
                skill.rmdir()

    def test_reports_correctly_targeted_broken_link(self) -> None:
        skill = self.add_published_skill("review", entrypoint=False)
        self.add_discovery_link("review")

        self.assertEqual(
            self.validate(skill),
            [".agents/skills/review: broken skill link; restore skills/review/SKILL.md"],
        )

    def test_reports_unexpected_legacy_discovery_link(self) -> None:
        legacy_target = self.repository_root / "legacy"
        legacy_target.mkdir()
        self.add_discovery_link("legacy", Path("../../legacy"))

        self.assertEqual(
            self.validate(),
            [
                ".agents/skills/legacy: unexpected symlink; "
                "only published skills may have discovery links"
            ],
        )

    def test_reports_missing_or_linked_internal_release(self) -> None:
        expected_error = ".agents/skills/release: preserve the internal skill as a real directory"
        release = self.discovery_root / "release"
        (release / "SKILL.md").unlink()
        release.rmdir()
        self.assertEqual(self.validate(), [expected_error])

        self.add_published_skill("release")
        self.add_discovery_link("release")
        self.assertIn(expected_error, self.validate())

    def test_validates_real_internal_release_content(self) -> None:
        release = self.discovery_root / "release"
        (release / "SKILL.md").write_text("not frontmatter\n", encoding="utf-8")

        self.assertEqual(
            self.validate(),
            [".agents/skills/release/SKILL.md: invalid frontmatter"],
        )

    def test_rejects_discovery_root_symlink(self) -> None:
        (self.discovery_root / "release" / "SKILL.md").unlink()
        (self.discovery_root / "release").rmdir()
        self.discovery_root.rmdir()
        alternate_root = self.repository_root / ".agents" / "linked-skills"
        alternate_root.mkdir()
        self.discovery_root.symlink_to("linked-skills", target_is_directory=True)

        self.assertEqual(
            self.validate(),
            [".agents/skills: must be a real directory containing discovery entries"],
        )


if __name__ == "__main__":
    unittest.main()
