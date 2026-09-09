# 添加项目内部发布 Skill

- 日期：2026-09-09
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-09-add-internal-release-skill.md`](../../exec-plans/completed/2026-09-09-add-internal-release-skill.md)

## 目标

在 `.agents/skills/release/` 提供本仓库可直接发现的内部发布 Skill，并在 `docs/release/` 集中维护
发布流程、版本日志规范与 GitHub Release 正文来源。

## 变更

- 新增内部 `release` Skill，区分只读规划、发布流程建设与“发布版本 X.Y.Z”的完整授权。
- 新增发布文档入口、流程说明和版本日志模板；未预先创建未发布版本的日志。
- tag workflow 在 npm 发布前验证同版本发布日志，使用它创建 GitHub Release，并补齐
  `worktree-rebase-merge` 单测。
- 更新资产结构说明，区分公开 `skills/` 与项目内部 `.agents/skills/`。

## 验证

- 仓库的 `validate_skill` 已针对 `.agents/skills/release/` 通过，发布文档和资产说明的相对链接通过。
- `python3 scripts/validate-skills.py` 验证 6 个公开 Skills 通过；
  `python3 scripts/validate-agents.py` 验证 4 个 Agents 通过。
- `python3 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`：2 项通过。
- Ruby YAML 解析 `publish.yml` 通过；`npm pack --dry-run --json` 仍只有 6 个 npm 文件，不含
  `.agents/` 或 `docs/`；`git diff --check` 通过。
- `skill-creator` 的 `quick_validate.py` 因环境缺少 `PyYAML` 无法启动；已使用仓库无依赖校验器替代。
- 独立 reviewer 审查通过，未发现阻塞 finding。未运行真实 GitHub Actions、npm 发布或外部安装，
  因此这些静态结果不证明线上发布或下游自动发现行为。

## 交付

- 本任务创建内部发布能力和文档；未修改版本、创建 tag、push、发布 npm 或创建 GitHub Release。
