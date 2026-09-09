# 明确 Planner 委派决策

- 日期：2026-09-09
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-09-clarify-planner-delegation.md`](../../exec-plans/completed/2026-09-09-clarify-planner-delegation.md)

## 目标

消除只读 planning 与独立 planner 委派之间的误读：涉及发布、部署、外部服务写入、跨模块取舍或
高风险变更的方案，必须先由只读 `planner` 提供独立规划结论。

## 变更

- 在 `docs/agents/request-boundary.md` 将任务模式与 planner 委派决策明确拆分。
- 增加按任务目标判定的决策表，涵盖明确请求、发布编排、跨模块取舍、高风险操作和低风险例外。
- 明确命中后必须等待结论再交付最终方案；用户禁止委派或子代理不可用时必须披露独立性缺失。
- 在根 `AGENTS.md` 保留单一规则来源，仅提醒每项任务作出委派决策。

## 验证

- 独立只读 planner 已审阅规则边界，确认无需修改 `planner.toml`、安装器或测试。
- `python3 scripts/validate-agents.py` 验证 4 个 Agents 通过；
  `python3 scripts/validate-skills.py` 验证 6 个 Skills 通过。
- Markdown 相对链接与 `Planner 委派决策` 标题检查通过；`git diff --check` 通过。

## 交付

- 本任务仅修改 Agent 治理文档；不执行发布、推送、外部服务写入或全局配置修改。
