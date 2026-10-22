<h1 align="center">Skills</h1>

<p align="center">
  <a href="./README.md">简体中文</a> ·
  <strong>English</strong>
</p>

A general-purpose collection of Agent Skills for software projects. It covers code simplification, Git commits, code review, pull request delivery, and worktree integration. Skills are installed with the [`skills`](https://github.com/vercel-labs/skills) CLI.

This repository is part of the agent development workflow for [Easydict](https://github.com/tisfeng/Easydict). Easydict uses the Skills published here for day-to-day development, code review, and Git delivery.

## Skill Catalog

| Skill | Purpose | Companion Skill |
| --- | --- | --- |
| [`code-simplifier`](skills/code-simplifier/SKILL.md) | Simplify recent code changes without altering behavior | None |
| [`git-commit`](skills/git-commit/SKILL.md) | Draft, create, or report validated Angular-style local commits | None |
| [`review`](skills/review/SKILL.md) | Review a working tree, commit, commit range, file, or module | None |
| [`review-pr`](skills/review-pr/SKILL.md) | Review exact GitHub pull request diffs, issue context, CI, and review threads | [`review`](skills/review/SKILL.md), plus [`git-commit`](skills/git-commit/SKILL.md) for naming |
| [`submit-pr`](skills/submit-pr/SKILL.md) | Plan, push, and create or reuse GitHub pull requests | [`git-commit`](skills/git-commit/SKILL.md) for naming, also reused when a commit is needed |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | Commit worktree changes, rebase them, and safely merge into a target branch | [`git-commit`](skills/git-commit/SKILL.md) |

A project's own `AGENTS.md`, build and validation configuration, and explicit user instructions take precedence over this repository's defaults; remote operations such as pushing, merging, publishing, or commenting run only with explicit user authorization.

Missing companion Skills are reported for the affected step without rewriting host rules. Branch naming requires a complete `git-commit` installation beside the consuming Skill; `submit-pr` also reuses its commit workflow when needed. Branch names follow the [shared naming policy](skills/git-commit/references/branch-naming.md), and `--head-branch` can keep a project's branch name. The Python interpreter used by a helper can be selected independently of the product runtime.

## Installation

Installing Skills requires Git. These commands can be repeated and always fetch the latest content from the repository's default branch.

### Project installation (default)

Install every published Skill in the current project:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

`--skill '*'` matches only the published Skills under `skills/`. Skills are written to `.agents/skills/` and recorded in `skills-lock.json`.

### Global installation

Install every published Skill in Codex's global directory:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills are written to `~/.agents/skills/`, and the lock file is stored at `~/.agents/.skill-lock.json`.

## License

[MIT](LICENSE)
