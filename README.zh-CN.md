# Skills

[English](README.md) | 简体中文

一组适用于大多数软件项目的通用 Agent Skills。技能以 Git、GitHub 和代码维护工作流为
主，支持通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装到 Codex 及其
他兼容 Agent。

## 技能目录

| Skill | 用途 | 配套 Skill |
| --- | --- | --- |
| `code-simplifier` | 在保持行为不变的前提下简化近期代码改动 | 无 |
| `git-commit` | 根据暂存区创建经过校验的 Angular-style 双语提交 | 无 |
| `review` | 审查工作树、提交、提交范围、文件或模块 | 无 |
| `review-pr` | 准备并审查 GitHub Pull Request，处理完整 review threads | `review` |
| `submit-pr` | 规划、推送并创建或复用 GitHub Pull Request | 需要提交时使用 `git-commit` |
| `worktree-rebase-merge` | 提交 worktree 变更，rebase 并安全合并到目标分支 | `git-commit` |

项目自己的 `AGENTS.md`、构建配置、验证规则和用户明确要求始终优先。各 skill 保留自己的
授权边界，不会因为被调用而自动获得 push、merge、评论或其他远程写入权限。

## 安装

本仓库是私有仓库。请先确保 Git、GitHub CLI 或 SSH 已经能够访问
`git@github.com:tisfeng/skills.git`。

查看可用技能：

```bash
npx skills add tisfeng/skills --list
```

将全部技能安装到 Codex 全局目录：

```bash
npx skills add tisfeng/skills --skill '*' --global --agent codex --yes
```

只为当前项目安装 PR review 组合：

```bash
npx skills add tisfeng/skills \
  --skill review \
  --skill review-pr \
  --agent codex \
  --yes
```

只为当前项目安装 worktree 交付组合：

```bash
npx skills add tisfeng/skills \
  --skill git-commit \
  --skill worktree-rebase-merge \
  --agent codex \
  --yes
```

默认安装范围是当前项目；`--global` 将技能安装到对应 Agent 的用户目录。Codex 的项目
目录是 `.agents/skills/`，全局目录是 `~/.codex/skills/`。

## 更新

更新当前项目安装的技能：

```bash
npx skills update --project
```

更新全局技能：

```bash
npx skills update --global
```

## 开发与验证

每个 skill 位于 `skills/<skill-name>/`，入口文件为 `SKILL.md`。修改后运行：

```bash
python3 scripts/validate-skills.py
python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'
python3 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'
python3 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'
bash -n skills/review-pr/scripts/prepare-pr-branch.sh
```

仓库的 GitHub Actions 会运行相同的结构、语法和单元测试检查。

## License

[MIT](LICENSE)
