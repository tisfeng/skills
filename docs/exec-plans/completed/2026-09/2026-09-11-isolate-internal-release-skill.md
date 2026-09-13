# 隔离仓库专属发布技能

- 状态：completed
- 创建日期：2026-09-11
- 负责人：main agent
- 关联 Issue/PR：none

## 背景

`release` 技能位于 `.agents/skills/`，而 `npx skills` 同时扫描 `skills/` 与 `.agents/skills/`。
消费者按 README 的 `--skill '*'` 安装会得到该技能，但它链接的 `docs/release/` 在消费项目中
不存在，且其请求语义针对本仓库的发布动作，存在误操作风险。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 目标结果：仓库专属技能移出技能发现路径，由校验器阻止回退，文档与安装示例同步
- 允许修改路径：`.agents/skills/`、`docs/agents/`、`docs/design-docs/overview.md`、
  `docs/release/overview.md`、`scripts/validate-skills.py`、`README.md`、`README.en.md`、
  `skills/git-commit/references/post-commit-report-example.md`、本计划、同任务 history
- 禁止动作：push、tag、GitHub Release、修改消费项目

## 目标与非目标

### 目标

- 把 `release` 移到发现路径之外并修正其相对链接。
- 让 `scripts/validate-skills.py` 拒绝发现路径中的非公开技能，并继续校验专属技能本体。
- 同步 `AGENTS.md`、治理与设计文档，安装示例改为显式公开技能名。

### 非目标

- 不改变发布流程本身，不新增或删除公开技能。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，校验 6 个公开技能与发现入口。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：通过。
- `npx skills add <repo> --list`：只发现 6 个公开技能。
- 负向用例：把专属技能放回 `.agents/skills/` 时校验器报错。
- 103 个 Markdown 文件的相对链接与锚点无失效；`git diff --check` 通过。

## 完成条件

- 上述验证通过，仓库差异只包含允许路径，本地提交完成。
