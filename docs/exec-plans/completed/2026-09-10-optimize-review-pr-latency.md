# 优化 review-pr 执行延迟

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex
- 同任务 history：[`docs/histories/2026-09/2026-09-10-optimize-review-pr-latency.md`](../../histories/2026-09/2026-09-10-optimize-review-pr-latency.md)

## 目标与授权

用户已授权实施此前给出的 `review-pr` 延迟优化方案。目标是在保留准确远程 head/base、完整
review thread 分页、本地分支保护、漂移处理和最终刷新门禁的前提下，减少模型往返、重复大输出
和不必要的本地全量验证。本任务只修改 `review-pr` Skill、辅助脚本、直接相关测试以及本计划和
history；不修改真实 PR、不 push，也不处理被审查 PR 中其他 Skill 的产品问题。

## 初始快照

- 初始 HEAD：`ab956382fcb8de8fe5254cd62d88b6f31b130b21`
- 初始分支：`review/pr-1-ab956382fc`
- 初始索引、工作树和未跟踪文件：均为空
- 交付方式：实现完成且验证通过后，按仓库规则候选自动本地提交；不 push

## 实现结果

1. 新增 `review_snapshot.py`，先冻结 PR 元数据和 head，再并行收集完整 threads/replies 与
   checks；输出完整初始证据、稳定 fingerprints、摘要和各阶段计时。
2. checks 查询以冻结 head 为前置锚点并在查询后复验，最终再与 PR/thread head 交叉校验；push
   交错时拒绝混合快照，不会错误复用其他提交的绿色 CI。
3. 最终 `refresh` 仍完整读取远程 PR、threads/replies 和 checks；无变化时只返回紧凑摘要，变化
   时展开对应完整 section，head 变化时展开全部证据。
4. Skill 正常路径改为复用快照、冻结一次 diff 证据、继续等待运行中会话、复用同一 head 的远程
   checks，并规定除非用户明确要求否则不等待 CI。
5. 线程维护文档明确复用初始完整 thread 快照；实际 resolve 前后的原有 fresh collect 与证据门禁
   不变。

## 风险与保护

- 并行 GitHub 读取不是事务。helper 通过初始 head 锚点、checks 后 head 复验、thread collector
  的末尾身份复验和跨 section head 比较缩小竞态窗口；发现不一致立即失败并要求重新收集。
- CI 失败或 pending 的 `gh pr checks` 非零退出码只作为结构化状态记录，不触发等待，也不误判成
  helper 成功路径中的绿色 CI。
- 紧凑刷新只减少向模型重复传输的内容，不减少底层远程读取和 thread/reply 分页。
- 远程 CI 只在准确同一 head 且完成通过时替代覆盖相同范围的广泛重复验证；finding、用户要求、
  仓库强制检查或覆盖缺口仍需针对性本地验证。

## 验证

- `review-pr` 35 项测试通过，其中新增 8 项覆盖完整快照、fingerprint、PR/thread/checks head 漂移、
  checks 查询期间 push、pending/failure 不等待、无变化压缩及变化展开。
- `python3.12 scripts/validate-skills.py` 通过，验证 6 个 Skill。
- `python3.12 -m compileall -q skills scripts` 和 `git diff --check` 通过。
- 真实只读 PR #1：完整 collect 约 6.23 秒；无变化 refresh 约 6.51 秒，返回 891 字符，同时底层
  仍完整刷新三类远程证据。
- 独立 reviewer 首轮发现 checks/head 绑定竞态；修复后确认该 finding 关闭，最终增量复核无新增
  finding。

## 完成条件

- 初始快照一次输出完整审查上下文和稳定 fingerprints：已完成。
- 无变化最终刷新不重复输出完整内容，变化时准确展开：已完成。
- 正常路径减少外层模型往返，禁止重复 diff、重启运行中测试或等待 CI：已完成。
- 直接相关测试、静态验证和独立复核通过：已完成。
