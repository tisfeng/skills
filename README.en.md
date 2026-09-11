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
| [`git-commit`](skills/git-commit/SKILL.md) | Create validated Angular-style bilingual commits from staged changes | None |
| [`review`](skills/review/SKILL.md) | Review a working tree, commit, commit range, file, or module | None |
| [`review-pr`](skills/review-pr/SKILL.md) | Prepare and review GitHub pull requests, including complete review threads | [`review`](skills/review/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | Plan, push, and create or reuse GitHub pull requests | [`git-commit`](skills/git-commit/SKILL.md) when a commit is needed |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | Commit worktree changes, rebase them, and safely merge into a target branch | [`git-commit`](skills/git-commit/SKILL.md) |

A project's own `AGENTS.md`, build and validation configuration, and explicit user instructions take precedence over this repository's defaults. Skills perform remote operations such as pushing, merging, publishing, or commenting only with explicit user authorization and when the applicable workflow conditions are satisfied.

Companion Skills are discovered from their actual load location, so a project does not need to copy this repository's agent documentation. `worktree-rebase-merge` confirms `git-commit` is available before its first Git write; `submit-pr` requires it only when a commit must be created, so an already committed clean branch can be planned or submitted on its own. When a companion capability is missing, the Skill reports the affected step instead of rewriting host rules.

Pull request submission uses a Conventional task branch by default and can keep a project's branch name through the existing `--head-branch` option; the Python interpreter used by a helper can be selected independently of the product runtime.

## Installation

Installing Skills requires Git. The commands below do not specify a tag, so they follow the repository's default branch; lock files record the source revision and content hashes actually installed.

### Project installation (default)

Install every Skill in the current project:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

Skills are written to `.agents/skills/` and recorded in `skills-lock.json`. Commit the lock file so the team uses the same source revisions and content.

### Global installation

Install every Skill in Codex's global directory:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills are written to `~/.codex/skills/`. The installer maintains its global lock file in the user's directories, so it does not need to be committed to a project repository.

## Updating

Routine upgrades only update installed assets and dependency records; they do not require a project to rewrite `AGENTS.md` or copy a Skill's internal workflow. Projects keep their own authorization, build, validation, and delivery policies, while Skills handle their own execution, validation, and failure handling. Only an incompatible change to a public entrypoint, required input, or supported dependency needs the matching migration note.

Update Skills installed for the current project:

```bash
npx skills update --project
```

Update global Skills:

```bash
npx skills update --global
```

## License

[MIT](LICENSE)
