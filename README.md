# Skills

简体中文 | [English](README.en.md)

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

## 安装

本仓库同时发布 Skills 和四个 Codex 自定义子代理：`planner`、`reviewer`、`tester` 与
`git-delivery`。二者使用独立的安装器和 lock 文件。

### 项目安装（默认）

在当前项目安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

在当前项目安装全部子代理：

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*'
```

Skills 写入 `.agents/skills/` 和 `skills-lock.json`；子代理写入 `.codex/agents/` 和
`.codex/agents-lock.json`。请将两个 lock 文件提交到版本控制，以保留团队所用的源码版本和内容哈希。

### 全局安装

在 Codex 全局目录安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

在 Codex 全局目录安装全部子代理：

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*' --global
```

Skills 写入 `~/.codex/skills/`；子代理写入 `~/.codex/agents/`。全局安装的 lock 文件分别位于
对应目录中。

## 更新

更新当前项目安装的 Skills 和子代理：

```bash
npx skills update --project
npx @tisfeng/codex-agents update
```

更新全局 Skills 和子代理：

```bash
npx skills update --global
npx @tisfeng/codex-agents update --global
```

若本地修改过子代理 TOML，安装器会拒绝覆盖与 lock 文件哈希不一致的文件；确认替换后，在对应的
`add` 或 `update` 命令末尾加入 `--force`。

## License

[MIT](LICENSE)
