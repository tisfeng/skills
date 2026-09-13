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
| [`git-commit`](skills/git-commit/SKILL.md) | 起草、创建或汇报经过校验的 Angular-style 本地提交 | 无 |
| [`review`](skills/review/SKILL.md) | 审查工作树、提交、提交范围、文件或模块 | 无 |
| [`review-pr`](skills/review-pr/SKILL.md) | 审查 GitHub Pull Request 的准确 diff、问题背景、CI 和 review threads | [`review`](skills/review/SKILL.md) |
| [`submit-pr`](skills/submit-pr/SKILL.md) | 规划、推送并创建或复用 GitHub Pull Request | 需要提交时使用 [`git-commit`](skills/git-commit/SKILL.md) |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | 提交 worktree 变更、执行 rebase，并安全合并到目标分支 | [`git-commit`](skills/git-commit/SKILL.md) |

项目的 `AGENTS.md`、构建与验证配置和用户明确指令优先于本仓库默认规则；push、merge、发布、
评论等远程操作只在用户明确授权后执行。

配套 Skill 从实际加载位置发现，缺失时报告受影响步骤，不改写宿主规则；`submit-pr` 只在需要
创建提交时依赖 `git-commit`。PR 提交默认使用 Conventional 任务分支，可用 `--head-branch`
沿用项目分支名；helper 的 Python 解释器可独立于产品运行时选择。

## 安装

安装需要 Git。以下命令未指定 tag，会跟随仓库默认分支；lock 文件记录实际安装的源码 revision
和内容哈希。

### 项目安装（默认）

在当前项目安装全部公开 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes
```

`--skill '*'` 只匹配 `skills/` 下的公开技能。Skills 写入 `.agents/skills/` 并记录在
`skills-lock.json` 中；请提交 lock 文件，确保团队使用相同的来源与内容。

### 全局安装

在 Codex 全局目录安装全部公开 Skills：

```bash
npx skills add tisfeng/skills --skill '*' --agent codex --yes --global
```

Skills 写入 `~/.codex/skills/`；全局 lock 由安装器维护，无需提交。

## 更新

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
