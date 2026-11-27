<h1 align="center">Skills</h1>

<p align="center">
  <a href="./README.md">简体中文</a> ·
  <strong>English</strong>
</p>

A general-purpose collection of Agent Skills for software projects. It covers code and documentation maintenance, code review, Git commits, PR delivery, and worktree integration. Skills are installed with the [`skills`](https://github.com/vercel-labs/skills) CLI.

This repository is part of the agent development workflow for [Easydict](https://github.com/tisfeng/Easydict). Easydict uses the Skills published here for day-to-day development, code review, and Git delivery.

## Skill Catalog

| Skill | Purpose | Companion Skill |
| --- | --- | --- |
| [`code-maintenance`](skills/code-maintenance/SKILL.md) | Maintain code and docs: simplify code, organize responsibilities, retire dead code, format Markdown, and check doc consistency | None |
| [`git-commit`](skills/git-commit/SKILL.md) | Draft, create, or report validated Angular-style local commits | None |
| [`review`](skills/review/SKILL.md) | Read-only review of local changes, commits, ranges, or modules for evidence-backed defects | None |
| [`review-pr`](skills/review-pr/SKILL.md) | Review exact GitHub PR diffs, linked issues, CI, and review threads | [`review`](skills/review/SKILL.md), [`git-commit`](skills/git-commit/SKILL.md) (naming) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | Preflight, push, and create or reuse a GitHub PR from committed changes | [`git-commit`](skills/git-commit/SKILL.md) (naming and commits) |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | Commit worktree changes, rebase onto the target branch, and merge locally | [`git-commit`](skills/git-commit/SKILL.md) |

> [!NOTE]
> The former `code-simplifier` skill is now part of `code-maintenance`. When upgrading, replace the old name in installation commands and project rules with `code-maintenance`.

- **Precedence and authorization**: A project's own `AGENTS.md`, build and validation configuration, and explicit user instructions take precedence over this repository's defaults; remote operations such as pushing, merging, publishing, or commenting run only with explicit user authorization.
- **Companion dependencies**: Missing companion Skills are reported for the affected step without rewriting host rules.

## Installation

Installing Skills requires Git. These commands can be repeated and always fetch the latest content from the repository's default branch.

### Project installation (default)

Install every published Skill in the current project:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

`--skill '*'` matches only the published Skills under `skills/`. Skills are written to `.agents/skills/` and recorded in `skills-lock.json`.

### Global installation

Install every published Skill globally:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills are written to `~/.agents/skills/`, and the lock file is stored at `~/.agents/.skill-lock.json`.

Replace `--agent` for another supported agent, or replace `--skill '*'` with a specific skill name to install individually.

## Additional Notes

- Branch names follow the [shared naming policy](skills/git-commit/references/branch-naming.md) and require a complete `git-commit` installation beside the consuming Skill; `submit-pr` also reuses its commit workflow when needed and supports `--head-branch` to keep a project's branch name.
- The Python interpreter used by bundled helper scripts can be selected independently of the target project's runtime.

## License

[MIT](LICENSE)
