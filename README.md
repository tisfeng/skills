# Skills

English | [简体中文](README.zh-CN.md)

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
| `submit-pr` | Plan, push, and create or reuse GitHub pull requests | `git-commit` when a commit is needed |
| `worktree-rebase-merge` | Commit worktree changes, rebase them, and safely merge into a target branch | `git-commit` |

A project's own `AGENTS.md`, build configuration, validation rules, and explicit user instructions
always take precedence. Each skill preserves its authorization boundaries and does not gain permission
to push, merge, comment, or perform other remote writes merely by being invoked.

## Installation

This is a private repository. Make sure Git, GitHub CLI, or SSH can access
`git@github.com:tisfeng/skills.git` before installing.

List the available skills:

```bash
npx skills add tisfeng/skills --list
```

Install every skill globally for Codex:

```bash
npx skills add tisfeng/skills --skill '*' --global --agent codex --yes
```

Install the pull-request review pair for the current project:

```bash
npx skills add tisfeng/skills \
  --skill review \
  --skill review-pr \
  --agent codex \
  --yes
```

Install the worktree delivery pair for the current project:

```bash
npx skills add tisfeng/skills \
  --skill git-commit \
  --skill worktree-rebase-merge \
  --agent codex \
  --yes
```

The default installation scope is the current project. `--global` installs skills in the selected
agent's user directory. Codex uses `.agents/skills/` for project installations and
`~/.codex/skills/` for global installations.

## Updating

Update skills installed in the current project:

```bash
npx skills update --project
```

Update globally installed skills:

```bash
npx skills update --global
```

## Development and Validation

Each skill lives in `skills/<skill-name>/` and uses `SKILL.md` as its entry point. Run the following
checks after making changes:

```bash
python3 scripts/validate-skills.py
python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'
python3 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'
python3 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'
bash -n skills/review-pr/scripts/prepare-pr-branch.sh
```

GitHub Actions runs the same structural, syntax, and unit-test checks.

## License

[MIT](LICENSE)
