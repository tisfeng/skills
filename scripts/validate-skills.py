#!/usr/bin/env python3
"""Validate the structure and local references of every published skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
NAME_PATTERN = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)
DESCRIPTION_PATTERN = re.compile(r"^description:\s*(?:\S|[>|])", re.MULTILINE)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CONFLICT_MARKER_PATTERN = re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
CATALOG_ROW_PATTERN = re.compile(r"^\|\s*`(?P<name>[a-z0-9-]+)`\s*\|", re.MULTILINE)


def validate_markdown_links(markdown_file: Path) -> list[str]:
    errors: list[str] = []
    markdown = markdown_file.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_PATTERN.findall(markdown):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#", "<")):
            continue
        resolved = (markdown_file.parent / target).resolve()
        if not resolved.exists():
            errors.append(
                f"{markdown_file.relative_to(REPOSITORY_ROOT)}: broken link {target}"
            )
    return errors


def validate_skill(skill_directory: Path) -> list[str]:
    errors: list[str] = []
    entrypoint = skill_directory / "SKILL.md"
    if not entrypoint.is_file():
        return [f"{skill_directory.relative_to(REPOSITORY_ROOT)}: missing SKILL.md"]

    text = entrypoint.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER_PATTERN.match(text)
    if frontmatter is None:
        errors.append(f"{entrypoint.relative_to(REPOSITORY_ROOT)}: invalid frontmatter")
        return errors

    frontmatter_body = frontmatter.group("body")
    name_match = NAME_PATTERN.search(frontmatter_body)
    if name_match is None:
        errors.append(f"{entrypoint.relative_to(REPOSITORY_ROOT)}: missing name")
    elif name_match.group(1).strip(' "\'') != skill_directory.name:
        errors.append(
            f"{entrypoint.relative_to(REPOSITORY_ROOT)}: name does not match directory"
        )

    if DESCRIPTION_PATTERN.search(frontmatter_body) is None:
        errors.append(f"{entrypoint.relative_to(REPOSITORY_ROOT)}: missing description")

    for markdown_file in skill_directory.rglob("*.md"):
        errors.extend(validate_markdown_links(markdown_file))

    return errors


def validate_conflict_markers() -> list[str]:
    errors: list[str] = []
    for path in REPOSITORY_ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if CONFLICT_MARKER_PATTERN.search(text):
            errors.append(f"{path.relative_to(REPOSITORY_ROOT)}: conflict marker found")
    return errors


def validate_readme_catalog(skill_directories: Sequence[Path]) -> list[str]:
    errors: list[str] = []
    expected_names = {directory.name for directory in skill_directories}
    for filename in ("README.md", "README.en.md"):
        readme = REPOSITORY_ROOT / filename
        if not readme.is_file():
            errors.append(f"{filename}: missing README")
            continue
        errors.extend(validate_markdown_links(readme))
        documented_names = set(CATALOG_ROW_PATTERN.findall(readme.read_text(encoding="utf-8")))
        missing = sorted(expected_names - documented_names)
        unknown = sorted(documented_names - expected_names)
        if missing:
            errors.append(f"{filename}: missing skills in catalog: {', '.join(missing)}")
        if unknown:
            errors.append(f"{filename}: unknown skills in catalog: {', '.join(unknown)}")
    return errors


def main() -> int:
    if not SKILLS_ROOT.is_dir():
        print("skills directory is missing", file=sys.stderr)
        return 1

    skill_directories = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    errors: list[str] = []
    names: set[str] = set()
    for skill_directory in skill_directories:
        if skill_directory.name in names:
            errors.append(f"duplicate skill directory: {skill_directory.name}")
        names.add(skill_directory.name)
        errors.extend(validate_skill(skill_directory))

    errors.extend(validate_readme_catalog(skill_directories))
    errors.extend(validate_conflict_markers())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_directories)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
