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

项目自己的 `AGENTS.md`、构建配置、验证规则和用户明确要求始终优先。各 skill 仅在当前
请求和自身工作流授权时执行 push、merge、评论或其他远程操作。

## Codex 子代理

本仓库还发布四个可版本化的 Codex 自定义子代理：`planner`、`reviewer`、`tester` 和
`git-delivery`。它们是 TOML 角色而非 Skill，因此使用独立的安装器与 lock 文件。项目级、
全局级、更新与本地定制保护见[子代理安装说明](docs/agent-installation.md)。

配套 npm 包发布后，可将全部子代理安装到当前项目：

```bash
npx @tisfeng/codex-agents add 'tisfeng/skills#v0.2.0' --agent '*'
```

加入 `--global` 可安装到 `~/.codex/agents/`。发布前，贡献者可直接运行仓库 CLI：
`node bin/codex-agents.mjs add . --list`。

## 安装

将全部技能安装到 Codex 全局目录：

```bash
npx skills add 'tisfeng/skills#v0.1.0' --skill '*' --global --agent codex --yes
```

将全部技能安装到当前项目：

```bash
npx skills add 'tisfeng/skills#v0.1.0' --skill '*' --agent codex --yes
```

默认安装范围是当前项目；`--global` 将技能安装到对应 Agent 的用户目录。Codex 的项目
目录是 `.agents/skills/`，全局目录是 `~/.codex/skills/`。

项目范围安装会生成 `skills-lock.json`。请将该文件提交到版本控制，以便团队固定所选
源码 ref 和内容哈希。

## 更新

更新当前项目安装的技能：

```bash
npx skills update --project
```

更新全局技能：

```bash
npx skills update --global
```

更新会保留安装时选择的源码 ref。固定到版本的安装会继续停留在该版本；需要升级时，请
使用更新的 tag 重新运行 `skills add`。

## 开发与验证

每个 skill 位于 `skills/<skill-name>/`，入口文件为 `SKILL.md`。修改后运行：

```bash
python3 scripts/validate-skills.py
python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'
python3 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'
python3 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'
bash -n skills/review-pr/scripts/prepare-pr-branch.sh
python3 scripts/validate-agents.py
node --test tests/agents-installer.test.mjs
```

仓库的 GitHub Actions 会运行相同的结构、语法和单元测试检查。

## License

[MIT](LICENSE)
