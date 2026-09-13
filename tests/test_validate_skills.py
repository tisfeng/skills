from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validate_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_skills
SPEC.loader.exec_module(validate_skills)


class FrontmatterValidationTests(unittest.TestCase):
    def validate(self, frontmatter: str, directory: str = "sample-skill") -> list[str]:
        return validate_skills.validate_frontmatter(
            frontmatter,
            directory,
            f"skills/{directory}/SKILL.md",
        )

    def test_accepts_required_fields(self) -> None:
        self.assertEqual(
            self.validate(
                "name: sample-skill\n"
                "description: Handle representative tasks when requested."
            ),
            [],
        )

    def test_rejects_invalid_required_fields(self) -> None:
        cases = {
            "missing name": (
                "description: Valid description.",
                "sample-skill",
                "missing name",
            ),
            "invalid name": (
                "name: sample--skill\ndescription: Valid description.",
                "sample--skill",
                "name must be 1-64",
            ),
            "long name": (
                f"name: {'a' * 65}\ndescription: Valid description.",
                "a" * 65,
                "name must be 1-64",
            ),
            "directory mismatch": (
                "name: another-skill\ndescription: Valid description.",
                "sample-skill",
                "name does not match directory",
            ),
            "missing description": (
                "name: sample-skill",
                "sample-skill",
                "missing description",
            ),
            "empty description": (
                'name: sample-skill\ndescription: ""',
                "sample-skill",
                "description must not be empty",
            ),
            "block description": (
                "name: sample-skill\ndescription: >-",
                "sample-skill",
                "description must use a single-line scalar",
            ),
            "long description": (
                f"name: sample-skill\ndescription: {'x' * 1025}",
                "sample-skill",
                "description exceeds 1024 characters",
            ),
            "duplicate description": (
                "name: sample-skill\n"
                "description: First.\n"
                "description: Second.",
                "sample-skill",
                "duplicate description",
            ),
        }
        for label, (frontmatter, directory, expected_error) in cases.items():
            with self.subTest(case=label):
                self.assertTrue(
                    any(
                        expected_error in error
                        for error in self.validate(frontmatter, directory)
                    ),
                    label,
                )


if __name__ == "__main__":
    unittest.main()
