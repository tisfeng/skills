# 补齐 review-pr 手动快照的 head 复验

- 日期：2026-09-10
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-fix-review-pr-fallback.md)

## 已落地变更

`review-pr` 原有总规则要求 checks 与 head 一致，但分散的手动回退命令没有明确落实查询后的
head 复验。本次在 `skills/review-pr/SKILL.md` 集中定义手动快照协议，初始采集和最终刷新
均引用该协议；独立诊断的 checks 在用于结论前同样需要重新绑定 head。

- 先冻结 PR 身份及 head，收集完整 threads/replies 和 checks，最后查询 head 并比较。
- 区分 helper 不可用与已检测到漂移；漂移后重新采集，再次漂移或读取仍失败时报告覆盖缺口。
- 手动初始快照没有 helper fingerprint 时，最终刷新比较完整证据，不要求伪造 fingerprint。
- 明确 checks 退出码与有效 JSON 的组合、空 checks 不作为绿色 CI 证据，保留默认不等待 CI。
- 正常 helper 实现和测试代码未变；手动回退依赖步骤可在同一次程序化编排内完成。

## 验证与限制

- `python3.12 scripts/validate-skills.py`：6 个 Skill 和发现入口通过。
- `PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：35 项通过。
- Skill Creator `quick_validate.py skills/review-pr`：通过；PyYAML 仅安装到任务临时目录供该检查使用。
- `git diff --check`：通过。
- 文档静态推演：稳定 head 可接受；采集中 push 拒绝混合快照；最终刷新到新 head 必须重新审查；
  head 查询失败不能复用 checks。持续漂移按停止条件报告缺口。
- 现有单测证明 helper 行为，静态推演检查手动指令；未执行真实 GitHub push 竞态或 Agent 运行评估。
- 使用 skill-creator 将回退规则集中维护，保留正常路径与既有功能。仅本地交付。
