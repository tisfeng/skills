# 优化 review-pr 的快照与编排延迟

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-optimize-review-pr-latency.md)

## 目标与变更

此前一次 `review-pr` 端到端约 10 分钟，主要耗时来自串行工具往返、重复传输完整 PR/diff/thread
内容、重复启动相同测试，以及在远程 CI 已有准确结果时再次执行广泛本地验证，而不是 GitHub
读取本身。

- 新增确定性的 review snapshot helper：先冻结 PR head，再并行收集完整分页的 threads/replies
  与 checks，一次返回初始完整证据、摘要、fingerprints 和计时。
- checks 使用冻结 head 锚点并在查询后复验；PR、threads 和 checks 之间的 head 不一致会拒绝
  快照，防止把旧提交的绿色 CI 绑定到新 head。
- 最终 refresh 保留三类远程状态的完整重读，无变化时仅返回紧凑摘要；变化时完整展开受影响
  section，head 漂移时展开全部证据并要求重新审查。
- Skill 规定同一 changed hunk 和上下文只读一次、运行中会话继续等待而不重启、同一 head 的已完成
  绿色 CI 可复用；失败或 pending 只报告状态，默认不等待 CI。
- thread resolve 的现有 fresh collect、fingerprint、远程 head 和 mutation 后读回规则全部保留。

## 验证

- `review-pr` 35 项行为测试通过；新增 8 项覆盖正常快照、三类 head 漂移、checks 查询期间 push、
  非零 checks 状态、fingerprint 和增量 refresh。
- 6 个 Skill 结构校验、全仓 Python compileall 和 `git diff --check` 通过。
- 对真实 PR #1 的只读 collect 约 6.23 秒；无变化 refresh 约 6.51 秒且仅返回 891 字符。
- 独立 reviewer 提出的 checks/head 竞态已经修复；最终增量复核无新的明确 finding。

## 交付边界

本任务只创建当前分支的本地提交，不 push、不等待 CI、不修改 PR #1 的评论、线程或 metadata，
也不 merge 到 `main`。真实性能收益仍受 GitHub 网络延迟和运行时模型调度影响；本次改动直接消除
的是可控的重复调用、重复输出和等待策略。
