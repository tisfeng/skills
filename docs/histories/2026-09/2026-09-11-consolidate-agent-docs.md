# 收敛 AGENTS.md 与 docs 治理文档

- 日期：2026-09-11
- 状态：completed
- 关联计划：none

## 目标

整体检查 `AGENTS.md` 与 `docs/` 后，按用户确认的方案修复入口碎片化和条款重复：把计划与
history 的命名约定和模板入口收敛到唯一权威位置，删除零入链的冗余子 README，并删除未接入
CI 的校验要求。同步修正检查中发现的重复条款与中英文 README 不同步。

这是单一领域的低风险文档修改，未命中 Planner 委派条件，也没有创建执行计划。

## 实际变更

- `docs/agents/README.md`：Plan 与 History 一节并入计划/历史的文件命名与模板链接，成为
  plan/history 生命周期、命名和模板的唯一来源。
- 删除 `docs/exec-plans/README.md`、`docs/histories/README.md`、`docs/release/README.md`
  三个零入链的二级索引。
- `AGENTS.md`：维护约束不再复述材料授权、Git 状态保护和文档生命周期条款，改为指向对应
  专题文件的唯一来源；新增版本发布流程路由。
- `docs/agents/build-and-test.md`：角色边界引用 `request-boundary.md` 的“子代理”一节，只
  保留验证收尾要求；删除未接入 CI 的 `tests/test_validate_skills.py` 要求。
- `README.en.md`：补齐中文 README 已有的配套 Skill 发现说明与常规升级承诺。

## 验证

- `git diff --check`：通过。
- `python3.12 scripts/validate-skills.py`：通过，校验 6 个 Skills 与发现入口。
- 全部 Markdown 相对链接与锚点扫描：通过，无断链或失效锚点。
- 被删除文件的入链复查：无现行规则或脚本引用，`.agents/skills/release/SKILL.md` 仍指向
  保留的 `docs/release/overview.md` 与 `docs/release/changelog/README.md`。

本轮未运行 npm 发布、GitHub 操作或将 Skills 安装到下游项目；静态检查只证明仓库内文档、
链接和脚本快照一致。

## 交付

仅在本仓库本地提交，不 push、不发布、不修改消费项目。
