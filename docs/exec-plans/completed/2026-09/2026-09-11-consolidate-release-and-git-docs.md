# 合并发布文档并重命名 Git 交付规则

- 状态：completed
- 创建日期：2026-09-11
- 负责人：main agent
- 关联 Issue/PR：none

## 背景

`docs/agents/release/SKILL.md` 与 `docs/release/overview.md` 互相引用：前者指向发布流程，
后者又把授权边界交给前者。该文件早已不是技能——技能发现路径只有 `skills/` 与
`.agents/skills/`，CLI 也只从这两处解析，因此它的 frontmatter 已是死配置。

同时 `docs/agents/git-workflow.md` 的实际内容是交付授权与门禁，没有分步工作流，文件名与
内容不符。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 目标结果：发布入口收敛为单文件；Git 交付规则改名；校验器拒绝发现路径之外的 `SKILL.md`
- 允许修改路径：`AGENTS.md`、`README.md`、`README.en.md`、`docs/agents/`、`docs/release/`、
  `docs/design-docs/overview.md`、`scripts/validate-skills.py`、本计划、同任务 history
- 禁止动作：push、tag、GitHub Release、修改消费项目

## 实际变更

- 合并为 `docs/release/workflow.md`，包含请求语义、准备、执行与恢复；删除
  `docs/release/overview.md` 与 `docs/agents/release/SKILL.md`，移除空目录。
- `docs/agents/git-workflow.md` 改名为 `docs/agents/git-delivery.md`，标题改为「Git 交付」。
- `scripts/validate-skills.py` 删除专属技能特例，新增 `SKILL.md` 位置守门。
- `AGENTS.md`、`docs/agents/README.md`、`docs/design-docs/overview.md` 与两份 README 同步到位。

## 验证

- `python3.12 scripts/validate-skills.py` 通过。
- 负向用例：在 `docs/` 下放入 `SKILL.md` 时校验器报错。
- 107 个 Markdown 文件的相对链接与锚点无失效；`git diff --check` 通过。
- `.agents/skills/` 仍只有 6 个公开技能链接。

## 完成条件

- 上述验证通过，仓库差异只包含允许路径，本地提交完成。
