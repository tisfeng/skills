<h1 align="center">Skills</h1>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="./README.en.md">English</a>
</p>

面向通用软件项目的 Agent Skills 集合，覆盖代码与文档维护、代码审查、Git 提交、PR 交付和 worktree 集成。Skills 通过 [`skills`](https://github.com/vercel-labs/skills) CLI 安装。

本仓库是 [Easydict](https://github.com/tisfeng/Easydict) Agent 开发流程的一部分；Easydict 使用这里发布的 Skills 组织日常开发、代码审查与 Git 交付。

## 技能目录

| Skill | 用途 | 配套 Skill |
| --- | --- | --- |
| [`code-maintenance`](skills/code-maintenance/SKILL.md) | 维护代码与文档：保行为简化代码、梳理文件职责、退役废弃代码、整理 Markdown 并核对文档一致性 | 无 |
| [`git-commit`](skills/git-commit/SKILL.md) | 起草、创建或汇报经过校验的 Angular-style 本地提交 | 无 |
| [`review`](skills/review/SKILL.md) | 只读审查本地变更、提交、范围或模块，识别有证据的缺陷与回归 | 无 |
| [`review-pr`](skills/review-pr/SKILL.md) | 审查 GitHub PR 的准确 diff、关联 Issue、CI 与 review threads | [`review`](skills/review/SKILL.md)、[`git-commit`](skills/git-commit/SKILL.md)（命名） |
| [`submit-pr`](skills/submit-pr/SKILL.md) | 基于已提交变更预检、推送并创建或复用 GitHub PR | [`git-commit`](skills/git-commit/SKILL.md)（命名与按需提交） |
| [`worktree-rebase-merge`](skills/worktree-rebase-merge/SKILL.md) | 提交 worktree 变更、rebase 到目标分支并安全完成本地合并 | [`git-commit`](skills/git-commit/SKILL.md) |

> [!NOTE]
> 原独立技能 `code-simplifier` 已并入 `code-maintenance`。升级时请将安装命令和项目规则中的旧名称改为 `code-maintenance`。

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

可按需替换 `--agent` 指定其他 Agent，或将 `--skill '*'` 替换为具体技能名单独安装。

## 补充说明

- **推荐用法**：`code-maintenance` 默认仅只读检查并给出建议方案（近 7 天、最多 50 个提交），推荐配置定时任务**每周运行一次**做例行巡检；也可随时指定文件或模块，明确要求执行代码重构、清理或 Markdown 整理。
- 分支命名统一遵循 [`git-commit` 命名规范](skills/git-commit/references/branch-naming.md)，依赖同级完整安装的 `git-commit`；`submit-pr` 创建提交时另复用其提交流程，并支持通过 `--head-branch` 沿用项目自定义分支名。
- Skill 附带的 Python helper 解释器可独立于目标项目的产品运行时选择。

## 许可证

[MIT](LICENSE)
