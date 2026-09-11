<h1 align="center">Skills</h1>

<p align="center">
  <a href="./README.md">简体中文</a> ·
  <strong>English</strong>
</p>

A general-purpose collection of Agent Skills and Codex custom-agent configurations for software projects. It covers code simplification, Git commits, code review, pull request delivery, and worktree integration. Skills are installed with the [`skills`](https://github.com/vercel-labs/skills) CLI; Codex custom agents are installed with `@tisfeng/codex-agents`.

This repository is part of the agent development workflow for [Easydict](https://github.com/tisfeng/Easydict). Easydict uses the Skills and Codex custom-agent configurations published here for day-to-day development, code review, and Git delivery.

## Skill Catalog

| Skill | Purpose | Companion Skill |
| --- | --- | --- |
| [`code-simplifier`](skills/code-simplifier/SKILL.md) | Simplify recent code changes without altering behavior | None |
| [`git-commit`](skills/git-commit/SKILL.md) | Create validated Angular-style bilingual commits from staged changes | None |
| [`review`](skills/review/SKILL.md) | Review a working tree, commit, commit range, file, or module | None |
| [`review-pr`](skills/review-pr/SKILL.md) | Prepare and review GitHub pull requests, including complete review threads | [`review`](skills/review/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | Plan, push, and create or reuse GitHub pull requests | [`git-commit`](skills/git-commit/SKILL.md) when a commit is needed |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | Commit worktree changes, rebase them, and safely merge into a target branch | [`git-commit`](skills/git-commit/SKILL.md) |

## Custom Agent Catalog

| Custom Agent | Purpose |
| --- | --- |
| [`planner`](.codex/agents/planner.toml) | Analyze requirements, evidence, and tradeoffs in read-only mode and recommend an implementation plan |
| [`reviewer`](.codex/agents/reviewer.toml) | Review a specified snapshot in read-only mode and report evidence-backed defects and suggested fixes |
| [`tester`](.codex/agents/tester.toml) | Write behavioral tests within the authorized scope and run targeted validation |

A project's own `AGENTS.md`, build and validation configuration, and explicit user instructions take precedence over this repository's defaults. Skills and custom agents perform remote operations such as pushing, merging, publishing, or commenting only with explicit user authorization and when the applicable workflow conditions are satisfied.

## Installation

Skills and Codex custom agents use different installers and maintain separate lock files.

Installing Codex custom agents requires Git and Node.js 20 or later. The commands below do not specify a tag, so they follow the repository's default branch; lock files record the source revision and content hashes actually installed.

### Project installation (default)

Install every Skill in the current project:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

Install every custom agent in the current project:

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*'
```

Skills are written to `.agents/skills/` and recorded in `skills-lock.json`; custom agents are written to `.codex/agents/` and recorded in `.codex/agents-lock.json`. Commit both lock files so the team uses the same source revisions and content.

### Global installation

Install every Skill in Codex's global directory:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Install every custom agent in Codex's global directory:

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*' --global
```

Skills are written to `~/.codex/skills/`; custom agents are written to `~/.codex/agents/`. Each installer maintains its global lock file in the user's directories, so these files do not need to be committed to a project repository.

## Updating

Update Skills and custom agents installed for the current project:

```bash
npx skills update --project
npx @tisfeng/codex-agents update
```

Update global Skills and custom agents:

```bash
npx skills update --global
npx @tisfeng/codex-agents update --global
```

## License

[MIT](LICENSE)
