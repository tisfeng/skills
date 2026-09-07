#!/usr/bin/env python3
"""Validate published Codex custom-agent TOML files and local references."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIRECTORY = ROOT / ".codex" / "agents"
REQUIRED_FIELDS = {
    "name": str,
    "description": str,
    "model": str,
    "model_reasoning_effort": str,
    "sandbox_mode": str,
    "developer_instructions": str,
}
VALID_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}


def main() -> int:
    errors: list[str] = []
    paths = sorted(AGENT_DIRECTORY.glob("*.toml"))
    if not paths:
        errors.append("no agent TOML files found")

    names: set[str] = set()
    for path in paths:
        try:
            with path.open("rb") as file:
                data = tomllib.load(file)
        except tomllib.TOMLDecodeError as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid TOML: {error}")
            continue

        for field, field_type in REQUIRED_FIELDS.items():
            value = data.get(field)
            if not isinstance(value, field_type) or not value.strip():
                errors.append(f"{path.relative_to(ROOT)}: missing non-empty {field}")
        name = data.get("name")
        if isinstance(name, str):
            if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
                errors.append(f"{path.relative_to(ROOT)}: invalid name {name!r}")
            if path.stem != name:
                errors.append(f"{path.relative_to(ROOT)}: filename must match name {name!r}")
            if name in names:
                errors.append(f"duplicate agent name: {name}")
            names.add(name)
        sandbox_mode = data.get("sandbox_mode")
        if sandbox_mode not in VALID_SANDBOX_MODES:
            errors.append(f"{path.relative_to(ROOT)}: unsupported sandbox_mode {sandbox_mode!r}")
        instructions = data.get("developer_instructions", "")
        if ".agents/skills/" in instructions or "Easydict" in instructions:
            errors.append(f"{path.relative_to(ROOT)}: contains a repository-specific dependency")

    if errors:
        print("Agent validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} agents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
