# Skills

[简体中文](README.md) | English

A collection of general-purpose Agent Skills designed for most software projects. The skills
focus on Git, GitHub, and code-maintenance workflows and can be installed for Codex and other
compatible agents through the [`skills`](https://github.com/vercel-labs/skills) CLI.

## Skill Catalog

| Skill | Purpose | Companion Skill |
| --- | --- | --- |
| `code-simplifier` | Simplify recent code changes without altering behavior | None |
| `git-commit` | Create validated Angular-style bilingual commits from staged changes | None |
| `review` | Review a working tree, commit, commit range, file, or module | None |
| `review-pr` | Prepare and review GitHub pull requests, including complete review threads | `review` |
| `submit-pr` | Plan, push, and create or reuse GitHub Pull Request | `git-commit` when a commit is needed |
| `worktree-rebase-merge` | Commit worktree changes, rebase them, and safely merge into a target branch | `git-commit` |

A project's own `AGENTS.md`, build configuration, validation rules, and explicit user instructions
always take precedence. Each skill performs remote actions only when the current request and its
workflow authorize them.

## Installation

This repository publishes both Skills and four Codex custom-agent configurations: `planner`,
`reviewer`, `tester`, and `git-delivery`. They use separate installers and lock files.

### Project installation (default)

Install every Skill in the current project:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

Install every custom agent in the current project:

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*'
```

Skills write to `.agents/skills/` and `skills-lock.json`; custom agents write to `.codex/agents/`
and `.codex/agents-lock.json`. Commit both lock files to preserve the source revision and content
hashes selected for the team.

### Global installation

Install every Skill in Codex's global directory:

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Install every custom agent in Codex's global directory:

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*' --global
```

Skills write to `~/.codex/skills/`; custom agents write to `~/.codex/agents/`. Their global lock
files are stored in the corresponding directories.

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

If a custom-agent TOML was modified locally, the installer refuses to overwrite a file whose hash
differs from the lock file. After reviewing the replacement, append `--force` to the relevant `add`
or `update` command.

## License

[MIT](LICENSE)
