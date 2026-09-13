"""Static contracts for clear Skill selection boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
CASES_PATH = REPOSITORY_ROOT / "tests" / "skill-trigger-cases.json"
DESCRIPTION_PATTERN = re.compile(r"^description:\s+(.+)$", re.MULTILINE)
CONFUSING_PAIRS = {
    frozenset(("code-simplifier", "review")),
    frozenset(("review", "review-pr")),
    frozenset(("review-pr", "submit-pr")),
    frozenset(("git-commit", "worktree-rebase-merge")),
}
GENERIC_RUNTIME_PROMPTS = (
    "程序化工具调用",
    "程序化工具编排",
    "退出码为 0",
    "`exit_code`",
    "运行中会话",
    "已加载且未变化",
    "已经加载且未变化",
)


def description_for(skill: str) -> str:
    text = (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
    match = DESCRIPTION_PATTERN.search(text)
    if match is None:
        raise AssertionError(f"{skill}: description must be a concise single line")
    return match.group(1).strip()


class SkillTriggerCaseTests(unittest.TestCase):
    def test_descriptions_are_short_and_name_confusing_alternatives(self) -> None:
        descriptions = {
            path.parent.name: description_for(path.parent.name)
            for path in SKILLS_ROOT.glob("*/SKILL.md")
        }
        for skill, description in descriptions.items():
            self.assertLessEqual(len(description), 100, f"{skill}: description is too long")

        for pair in CONFUSING_PAIRS:
            first, second = tuple(pair)
            self.assertIn(second, descriptions[first], f"{first}: missing boundary with {second}")
            self.assertIn(first, descriptions[second], f"{second}: missing boundary with {first}")

    def test_cases_cover_both_directions_of_each_confusing_pair(self) -> None:
        payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        observed_pairs = {frozenset(group["skills"]) for group in payload["pairs"]}
        self.assertEqual(observed_pairs, CONFUSING_PAIRS)

        published = {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}
        ids: set[str] = set()
        for group in payload["pairs"]:
            pair = set(group["skills"])
            self.assertEqual({case["expected_skill"] for case in group["cases"]}, pair)
            for case in group["cases"]:
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                self.assertIn(case["expected_skill"], published)
                self.assertTrue(pair - {case["expected_skill"]} <= set(case["excluded_skills"]))
                self.assertTrue(case["request"].strip())
                self.assertTrue(case["why"].strip())

    def test_skill_docs_do_not_reteach_generic_runtime_orchestration(self) -> None:
        for markdown in SKILLS_ROOT.glob("**/*.md"):
            text = markdown.read_text(encoding="utf-8")
            for prompt in GENERIC_RUNTIME_PROMPTS:
                self.assertNotIn(prompt, text, f"{markdown.relative_to(REPOSITORY_ROOT)}: {prompt}")


if __name__ == "__main__":
    unittest.main()
