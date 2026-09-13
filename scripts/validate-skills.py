#!/usr/bin/env python3
"""Validate published skills, local references, and repository discovery entries."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CONFLICT_MARKER_PATTERN = re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
LINKED_CATALOG_ROW_PATTERN = re.compile(
    r"^\|\s*\[`(?P<name>[a-z0-9-]+)`\]\((?P<target>[^)\n]+)\)\s*\|",
    re.MULTILINE,
)
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def required_frontmatter_scalar(
    frontmatter: str,
    field: str,
    label: str,
) -> tuple[str | None, list[str]]:
    """Read one required, repository-supported single-line YAML scalar."""

    matches = re.findall(
        rf"^{re.escape(field)}:[ \t]*(.*)$",
        frontmatter,
        re.MULTILINE,
    )
    if not matches:
        return None, [f"{label}: missing {field}"]
    if len(matches) > 1:
        return None, [f"{label}: duplicate {field}"]

    value = matches[0].strip()
    if value.startswith(("|", ">")):
        return None, [f"{label}: {field} must use a single-line scalar"]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    if not value:
        return None, [f"{label}: {field} must not be empty"]
    return value, []


def validate_frontmatter(frontmatter: str, directory_name: str, label: str) -> list[str]:
    """Validate the deterministic Agent Skills metadata used by this repository."""

    errors: list[str] = []
    name, field_errors = required_frontmatter_scalar(frontmatter, "name", label)
    errors.extend(field_errors)
    if name is not None:
        if len(name) > MAX_NAME_LENGTH or SKILL_NAME_PATTERN.fullmatch(name) is None:
            errors.append(
                f"{label}: name must be 1-{MAX_NAME_LENGTH} lowercase letters, "
                "numbers, or single hyphens"
            )
        if name != directory_name:
            errors.append(f"{label}: name does not match directory")

    description, field_errors = required_frontmatter_scalar(
        frontmatter, "description", label
    )
    errors.extend(field_errors)
    if description is not None and len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"{label}: description exceeds {MAX_DESCRIPTION_LENGTH} characters"
        )

    return errors


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

    label = str(entrypoint.relative_to(REPOSITORY_ROOT))
    errors.extend(
        validate_frontmatter(frontmatter.group("body"), skill_directory.name, label)
    )

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


def validate_discovery_entries(skill_directories: Sequence[Path]) -> list[str]:
    errors: list[str] = []
    discovery_root = REPOSITORY_ROOT / ".agents" / "skills"
    if discovery_root.is_symlink() or not discovery_root.is_dir():
        return [".agents/skills: must be a real directory containing discovery entries"]

    published_names = {directory.name for directory in skill_directories}
    for name in sorted(published_names):
        entry = discovery_root / name
        label = entry.relative_to(REPOSITORY_ROOT)
        expected_target = Path("../../skills") / name
        if not entry.is_symlink():
            errors.append(f"{label}: create a relative symlink to {expected_target}")
        elif entry.readlink() != expected_target:
            errors.append(f"{label}: symlink must target {expected_target}")
        elif not (entry / "SKILL.md").is_file():
            errors.append(f"{label}: broken skill link; restore skills/{name}/SKILL.md")

    for entry in sorted(discovery_root.iterdir()):
        if entry.name in published_names:
            continue
        errors.append(
            f"{entry.relative_to(REPOSITORY_ROOT)}: keep repository-specific skills out of the "
            "discovery path so installers cannot copy them into consumer projects"
        )
    return errors


def validate_skill_locations() -> list[str]:
    """Keep SKILL.md inside the published tree or its discovery links."""

    errors: list[str] = []
    allowed_roots = (
        SKILLS_ROOT.resolve(),
        (REPOSITORY_ROOT / ".agents" / "skills").resolve(),
    )
    for entrypoint in REPOSITORY_ROOT.rglob("SKILL.md"):
        if ".git" in entrypoint.parts:
            continue
        resolved = entrypoint.resolve()
        if any(root in resolved.parents for root in allowed_roots):
            continue
        errors.append(
            f"{entrypoint.relative_to(REPOSITORY_ROOT)}: keep SKILL.md inside skills/ "
            "or .agents/skills/"
        )
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
        linked_entries = LINKED_CATALOG_ROW_PATTERN.findall(
            readme.read_text(encoding="utf-8")
        )
        skill_entries = [
            (name, target)
            for name, target in linked_entries
            if name in expected_names or target.startswith("skills/")
        ]
        documented_names = {name for name, _ in skill_entries}
        missing = sorted(expected_names - documented_names)
        unknown = sorted(documented_names - expected_names)
        if missing:
            errors.append(f"{filename}: missing skills in catalog: {', '.join(missing)}")
        if unknown:
            errors.append(f"{filename}: unknown skills in catalog: {', '.join(unknown)}")
        for name, target in skill_entries:
            if name in expected_names:
                expected_target = f"skills/{name}/SKILL.md"
                if target != expected_target:
                    errors.append(
                        f"{filename}: {name} must link to {expected_target}, found {target}"
                    )
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

    errors.extend(validate_discovery_entries(skill_directories))
    errors.extend(validate_readme_catalog(skill_directories))
    errors.extend(validate_skill_locations())
    errors.extend(validate_conflict_markers())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_directories)} skills and repository discovery entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
