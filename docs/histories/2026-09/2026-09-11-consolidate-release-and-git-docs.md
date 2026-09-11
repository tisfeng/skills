# 合并发布文档并重命名 Git 交付规则

- 日期：2026-09-11
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-11-consolidate-release-and-git-docs.md`](../../exec-plans/completed/2026-09-11-consolidate-release-and-git-docs.md)

## 目标

用户指出发布入口已不再是技能，不应继续叫 `SKILL.md`，且与 `overview.md` 重复；同时认为
`git-workflow.md` 的名字与内容不符。本任务合并发布文档、改名交付规则，并把边界写进校验器。

## 实际变更

- 新增 `docs/release/workflow.md`，内容为合并后的请求语义、准备、执行与恢复；删除
  `docs/release/overview.md` 和 `docs/agents/release/SKILL.md`，并移除空的
  `docs/agents/release/` 目录。
- `docs/agents/git-workflow.md` 改名为 `docs/agents/git-delivery.md`，一级标题改为「Git 交付」。
- `scripts/validate-skills.py`：删除 `docs/agents/release` 专属校验，新增 `SKILL.md` 位置
  守门——只允许出现在 `skills/` 与 `.agents/skills/`，其余位置直接报错。
- `AGENTS.md` 两处路由、`docs/agents/README.md` 的文档分层与源码资产边界、
  `docs/design-docs/overview.md` 的结构表，以及两份 README 的 `--skill '*'` 说明同步更新。

## 验证

- `python3.12 scripts/validate-skills.py` 通过；负向用例（`docs/` 下放置 `SKILL.md`）按预期报错。
- 全仓 107 个 Markdown 文件的相对链接与锚点无失效；`git diff --check` 通过。
- `.agents/skills/` 仍只包含 6 个公开技能链接，发布文档不再参与技能发现。

## 交付

仅在本仓库本地提交；未 push、未创建 tag 或 GitHub Release，未修改消费项目。
