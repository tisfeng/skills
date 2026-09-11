<h1 align="center">Skills</h1>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="./README.en.md">English</a>
</p>

面向通用软件项目的 Agent Skills 集合，覆盖代码简化、Git 提交、代码审查、Pull Request 交付和 worktree 集成。Skills 通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装。

本仓库是 [Easydict](https://github.com/tisfeng/Easydict) Agent 开发流程的一部分；Easydict 使用这里发布的 Skills 组织日常开发、代码审查与 Git 交付。

## 技能目录

| Skill | 用途 | 配套 Skill |
| --- | --- | --- |
| [`code-simplifier`](skills/code-simplifier/SKILL.md) | 在保持行为不变的前提下简化近期代码改动 | 无 |
| [`git-commit`](skills/git-commit/SKILL.md) | 从暂存区创建经过校验的 Angular-style 双语提交 | 无 |
| [`review`](skills/review/SKILL.md) | 审查工作树、提交、提交范围、文件或模块 | 无 |
| [`review-pr`](skills/review-pr/SKILL.md) | 准备并审查 GitHub Pull Request，完整处理 review threads | [`review`](skills/review/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | 规划、推送并创建或复用 GitHub Pull Request | 需要提交时使用 [`git-commit`](skills/git-commit/SKILL.md) |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | 提交 worktree 变更、执行 rebase，并安全合并到目标分支 | [`git-commit`](skills/git-commit/SKILL.md) |

项目的 `AGENTS.md`、构建与验证配置以及用户明确指令优先于本仓库的默认规则。涉及 push、merge、发布、评论等远程操作时，Skills 只会在用户明确授权且相应工作流条件满足后执行。

配套 Skill 按实际加载位置发现，不要求项目复制本仓库 Agent 文档。`worktree-rebase-merge`
在首次 Git 写入前确认 `git-commit` 可用；`submit-pr` 仅在需要创建提交时要求它，干净的已有
提交可直接规划或提交 PR。缺少配套能力时报告受影响步骤，不改写宿主规则。
PR 提交默认使用 Conventional 任务分支，也可通过现有 `--head-branch` 参数沿用项目分支名；
工具所需的 Python 解释器可以独立于产品运行时选择。

## 安装

安装 Skills 需要 Git。以下命令未指定 tag，会跟随仓库默认分支；lock 文件记录实际安装的源码 revision 和内容哈希。

### 项目安装（默认）

在当前项目安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

Skills 写入 `.agents/skills/`，并在 `skills-lock.json` 中记录版本。请将 lock 文件提交到版本控制，确保团队使用相同的来源版本和内容。

### 全局安装

在 Codex 全局目录安装全部 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills 写入 `~/.codex/skills/`；全局 lock 文件由安装器在用户目录中维护，无需提交到项目仓库。

## 更新

常规升级只更新安装资产与依赖记录，不要求项目改写 `AGENTS.md` 或复制 Skill 的内部流程。
项目继续维护自己的授权、构建、验证和交付政策；Skill 负责自身执行、校验和失败处理。
公开入口、必填输入或支持依赖发生不兼容变化时，才需要按对应迁移说明处理。

更新当前项目安装的 Skills：

```bash
npx skills update --project
```

更新全局 Skills：

```bash
npx skills update --global
```

## 许可证

[MIT](LICENSE)
