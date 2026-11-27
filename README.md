<h1 align="center">Skills</h1>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="./README.en.md">English</a>
</p>

面向通用软件项目的 Agent Skills 集合，覆盖代码与文档维护、本地与 PR 代码审查、Git 提交、Pull Request 交付和 worktree 集成。Skills 通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装。

本仓库是 [Easydict](https://github.com/tisfeng/Easydict) Agent 开发流程的一部分；Easydict 使用这里发布的 Skills 组织日常开发、代码审查与 Git 交付。

## 技能目录

| Skill | 用途 | 配套 Skill |
| --- | --- | --- |
| [`code-maintenance`](skills/code-maintenance/SKILL.md) | 维护近期或指定范围的代码与文档：保行为简化冗余逻辑、梳理文件职责、核验并退役废弃代码、整理 Markdown 排版，并双向核对代码与现行文档的一致性（含 Swift/Xcode、Electron/TypeScript 专项指南） | 无 |
| [`git-commit`](skills/git-commit/SKILL.md) | 校验 staged 范围并起草、创建或汇报 Angular-style 本地 Git 提交 | 无 |
| [`review`](skills/review/SKILL.md) | 只读审查本地工作树、提交、提交范围、文件或模块，基于代码证据识别缺陷、回归与实现方式问题 | 无 |
| [`review-pr`](skills/review-pr/SKILL.md) | 审查 GitHub Pull Request 的准确 head/base diff、关联 Issue、CI 状态与 review threads，在授权范围内回复并关闭已解决线程 | [`review`](skills/review/SKILL.md)、命名使用 [`git-commit`](skills/git-commit/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | 基于当前已提交变更预检、规划、推送并创建或复用 GitHub Pull Request（支持 Draft 与验证截图复用） | 命名依赖 [`git-commit`](skills/git-commit/SKILL.md)，需要提交时复用其提交流程 |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | 提交当前 worktree 变更、rebase 到目标分支，并从目标 worktree 安全完成本地合并 | [`git-commit`](skills/git-commit/SKILL.md) |

> [!NOTE]
> 原独立技能 `code-simplifier` 已并入 `code-maintenance`。从旧版本升级时，请将安装命令、项目规则及工作流中的旧名称替换为 `code-maintenance`。

- **规则优先级与授权**：项目的 `AGENTS.md`、构建与验证配置以及用户明确指令优先于本仓库默认规则；push、merge、发布、评论等远程操作仅在用户明确授权后执行。
- **配套依赖**：配套 Skill 缺失时会如实报告受影响步骤，不改写宿主规则。

## 安装

安装需要 Git。以下命令可重复执行，每次都会获取仓库默认分支的最新内容。

### 项目安装（默认）

在当前项目安装全部公开 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

`--skill '*'` 只匹配 `skills/` 下的公开技能。Skills 写入 `.agents/skills/` 并记录在 `skills-lock.json` 中。

### 全局安装

在全局目录安装全部公开 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills 写入 `~/.agents/skills/`，lock 位于 `~/.agents/.skill-lock.json`。

如需安装到其他支持的 Agent，可将 `--agent codex` 替换为对应 Agent 名称；如需按需安装单个技能，可将 `--skill '*'` 替换为具体技能名（例如 `--skill code-maintenance`）。

## 补充说明

- 分支命名统一遵循 [`git-commit` 命名规范](skills/git-commit/references/branch-naming.md)，依赖同级完整安装的 `git-commit`；`submit-pr` 创建提交时另复用其提交流程，并支持通过 `--head-branch` 沿用项目自定义分支名。
- Skill 附带的 Python helper 解释器可独立于目标项目的产品运行时选择。

## 许可证

[MIT](LICENSE)
