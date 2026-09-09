# 复用工作流证据并减少重复查询

- 状态：completed
- 日期：2026-09-10

## 目标与授权

用户批准延迟优化方案，复用上一轮已完成的独立规划。明确规划结论、验证结果与子代理续办
信息的复用边界，并减少 submit-pr 单次拓扑发现中的重复查询；不改变模型、权限或交付契约。
本任务为 implementation，采用 auto-local-commit，由主 Agent 本地交付，不 push 或操作真实 PR。

## 初始状态与范围

- 初始 HEAD：`062df9be9eda2191609d4cd0a1b761c239bfbc0a`，分支 `main`。
- staged、unstaged、untracked 和冲突均为空；写入前检查通过。
- 允许路径：`docs/agents/request-boundary.md`、`docs/agents/build-and-test.md`、
  `skills/submit-pr/scripts/submit_pr.py`、`skills/submit-pr/tests/test_submit_pr.py`、
  `skills/submit-pr/references/workflow.md`、本计划及同名 history。实际改动均由主 Agent 负责。
- history：`docs/histories/2026-09/2026-09-10-reuse-workflow-evidence.md`。

## 实施与验收

1. 补充相同任务下有效规划和验证证据的复用条件，以及子代理增量交接规则。
2. 复用本次已查询的仓库元数据，保持新调用重新发现及写入前后校验。
3. 用隔离 Git/GitHub fixture 验证显式参数、环境变量、大小写、未知别名及 plan/apply 刷新。
4. 运行相关测试、结构/链接与编译检查，独立复核后更新 history、归档计划并精确提交。

只减少已证实的重复工作，不以少跑检查或减少请求数替代正确性；不声称测得整体延迟降幅。

## 验证结果

26 项 submit-pr 测试、6 个 Skill 与 3 个子代理结构校验、submit-pr quick_validate 和 Python
编译通过；独立只读复核无 finding。新增用例先在旧实现的四个参数场景复现重复查询，修复后
验证一次查询、未命中别名仍请求 API，以及远程默认分支变化后的 apply 刷新。
