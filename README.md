<h1 align="center">Skills</h1>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="./README.en.md">English</a>
</p>

面向通用软件项目的 Agent Skills 与 Codex 子代理配置集合，覆盖代码简化、Git 提交、代码审查、Pull Request 交付和 worktree 集成。Skills 通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装；Codex 子代理通过 `@tisfeng/codex-agents` 安装。

本仓库是 [Easydict](https://github.com/tisfeng/Easydict) Agent 开发流程的一部分；Easydict 使用这里发布的 Skills 和 Codex 子代理配置组织日常开发、代码审查与 Git 交付。

## 技能目录

| Skill | 用途 | 配套 Skill |
| --- | --- | --- |
| [`code-simplifier`](skills/code-simplifier/SKILL.md) | 在保持行为不变的前提下简化近期代码改动 | 无 |
| [`git-commit`](skills/git-commit/SKILL.md) | 从暂存区创建经过校验的 Angular-style 双语提交 | 无 |
| [`review`](skills/review/SKILL.md) | 审查工作树、提交、提交范围、文件或模块 | 无 |
| [`review-pr`](skills/review-pr/SKILL.md) | 准备并审查 GitHub Pull Request，完整处理 review threads | [`review`](skills/review/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | 规划、推送并创建或复用 GitHub Pull Request | 需要提交时使用 [`git-commit`](skills/git-commit/SKILL.md) |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | 提交 worktree 变更、执行 rebase，并安全合并到目标分支 | [`git-commit`](skills/git-commit/SKILL.md) |

## 子代理目录

| 子代理 | 用途 |
| --- | --- |
| [`planner`](.codex/agents/planner.toml) | 只读分析需求、证据与取舍，输出实施建议 |
| [`reviewer`](.codex/agents/reviewer.toml) | 只读审查指定快照，提供有证据的缺陷与修复建议 |
| [`tester`](.codex/agents/tester.toml) | 在授权范围内编写行为测试并执行针对性验证 |
| [`git-delivery`](.codex/agents/git-delivery.toml) | 串行执行已授权的本地提交与 worktree 集成，不执行 push |

项目的 `AGENTS.md`、构建与验证配置以及用户明确指令优先于本仓库的默认规则。涉及 push、merge、发布、评论等远程操作时，Skills 与子代理只会在用户明确授权且相应工作流条件满足后执行。

## 安装

Skills 与 Codex 子代理使用不同的安装器，并分别维护自己的 lock 文件。

安装 Codex 子代理需要 Git 和 Node.js 20 或更高版本。以下命令未指定 tag，会跟随仓库默认分支；lock 文件记录实际安装的源码 revision 和内容哈希。

### 项目安装（默认）

在当前项目安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

在当前项目安装全部子代理：

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*'
```

Skills 写入 `.agents/skills/`，并在 `skills-lock.json` 中记录版本；子代理写入 `.codex/agents/`，并在 `.codex/agents-lock.json` 中记录版本。请将两个 lock 文件提交到版本控制，确保团队使用相同的来源版本和内容。

### 全局安装

在 Codex 全局目录安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

在 Codex 全局目录安装全部子代理：

```bash
npx @tisfeng/codex-agents add tisfeng/skills --agent '*' --global
```

Skills 写入 `~/.codex/skills/`；子代理写入 `~/.codex/agents/`。全局 lock 文件由各安装器在用户目录中维护，无需提交到项目仓库。

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

若本地修改过子代理 TOML，安装器会拒绝覆盖与 lock 文件哈希不一致的文件。确认需要替换后，在对应的 `add` 或 `update` 命令末尾加入 `--force`。

## 许可证

[MIT](LICENSE)
