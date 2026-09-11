# 隔离仓库专属发布技能

- 日期：2026-09-11
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-11-isolate-internal-release-skill.md`](../../exec-plans/completed/2026-09-11-isolate-internal-release-skill.md)

## 目标

复查公开技能与发布技能后，确认 6 个公开技能不依赖已删除的子代理，但 `release` 会被
`npx skills` 安装到消费项目并在那里失效。本任务把该技能移出发现路径并加上防回退校验。

## 实际变更

- 移动 `.agents/skills/release/SKILL.md` 到 `docs/agents/release/SKILL.md`，并改为指向
  `../../release/` 的相对链接；删除残留的空目录。
- `scripts/validate-skills.py`：发现路径中出现任何非公开条目即报错，并改为校验
  `docs/agents/release/` 下的专属技能。
- `AGENTS.md`、`docs/agents/README.md`、`docs/design-docs/overview.md`、
  `docs/release/overview.md` 同步新的技能位置与发现路径边界。
- `README.md` 与 `README.en.md` 的安装示例改为显式列出 6 个公开技能，不再使用 `--skill '*'`。
- `skills/git-commit/references/post-commit-report-example.md` 的示例分支名改为不含已删概念的
  `docs/unify-commit-receipts`。

## 验证

- `python3.12 scripts/validate-skills.py` 通过；隔离消费者测试通过。
- `npx skills add <repo> --list` 从 7 个降为 6 个，`release` 不再出现。
- 负向用例：在 `.agents/skills/` 放入专属技能时校验器报错。
- 全仓 103 个 Markdown 文件的相对链接与锚点无失效，`git diff --check` 通过。

## 交付

仅在本仓库本地提交；未 push、未创建 tag 或 GitHub Release，未修改消费项目。

## 后续调整

安装示例恢复为一行 `--skill '*'`。结构性隔离与校验器守门完成后，实测 `--skill '*'` 只安装
6 个公开技能，`release` 不再出现；显式列举 6 个技能名的写法因此既无必要又过长，仅在说明中
保留「发布会话之外」的边界提示。
