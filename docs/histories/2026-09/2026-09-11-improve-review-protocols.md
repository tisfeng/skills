# 改进 review 与 review-pr 的快照和执行协议

## 背景与范围

用户批准对两个技能的前两批优化，要求保留完整审查、安全检查、报告和 CI 默认不等待。
本轮从 `053509d8a4b4efcf3673482630490df2fee8b1e0` 的干净任务分支实施，仅修改这两个技能的
源码、参考协议、测试及同任务文档；不改 main，不 push，不操作真实 PR 或全局安装。

执行计划：[改进 review 执行协议](../../exec-plans/completed/2026-09-11-improve-review-protocols.md)。

## 已落地

- PR 空白检查显式使用冻结 merge-base/head；PR 复用 review 的 range 快照，集成结果与远程 head 分开。
- 最终刷新识别 base 名称/SHA 变化，明确 retarget 和 base 前进时的范围复验与增量审查。
- 准备 helper 增加 expected-head、版本化 JSON 回执及可选的哈希绑定元数据复用；保留旧 CLI。
  同一轮 head/base 各 fetch 一次，实际 fetch 校验、冲突分支保护与 worktree 校验不省略。
- 完整远程证据可以保存到独占创建的私有任务文件，分页带完整性哈希和连续覆盖字段；续页不联网。
- 最终刷新保留完整远程读取，仅对模型输出变化线程正文、移除清单和全量索引；旧证据损坏/不匹配
  时回退全量。checks 集合和线程列表的无意义顺序变化不再触发指纹变化，评论顺序仍属于证据。
- resolve 前后改为核验请求 PR 和目标线程全部回复；包含父 PR 身份、分页结束的状态/回复数校验。
  初始与最终全量刷新、权限检查、漂移停止及未知 mutation 结果处理继续保留。

线程归属查询使用 GitHub 公布的 `PullRequestReviewThread.pullRequest` 字段；字段核实参考
[GitHub GraphQL schema](https://docs.github.com/en/graphql/reference/pulls#pullrequestreviewthread)。
本轮没有加入本地 diff 缓存：已测量的本地 Git 成本不足以支持增加该复杂度。

## 验证与独立评估

- 复用上一轮独立 Planner 的同范围结论；独立 reviewer 未发现需修复的 P0–P3 finding。
- `python3.12 -B -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：67 项通过。
- `python3.12 -B -m unittest discover -s skills/review/tests -p 'test_*.py'`：10 项通过。
- 加强同一组评论仅交换顺序的断言后，`test_review_snapshot.py` 的 17 项增量复验通过。
- `python3.12 scripts/validate-skills.py`、两个 Skill 的 quick_validate、Python compileall、
  `bash -n` 和 `git diff --check` 均通过。quick_validate 所需 PyYAML 仅安装到任务临时目录，
  未增加项目或全局依赖。
- fake gh + 临时 Git 仓库验证普通、合并和 worktree 模式的真实 fetch 调用次数；缓存元数据路径
  不调用 `gh pr view`，但仍拒绝 fetch 到不同 head。
- 模拟 10 条 resolve 时，旧实现读取 200 条线程记录，新实现仅定向读取 20 条；每条前后检查保留。
- 模拟 200 条线程、1 条正文变化时，完整刷新 JSON 为 627876 字节，差量为 31937 字节，减少 94.9%。
  该数字只证明同一 fixture 下的传输量变化，不表示真实 Agent 端到端耗时同比下降。

## 边界

测试全部使用 fake API/临时仓库，没有真实 PR resolve、CI 等待、push、发布或下游安装验证。
GraphQL 分页与 resolve 没有原子 CAS；前后守卫减少竞态，但不声称消除所有并发窗口。
真实网络与模型运行时的端到端提速仍需后续实际使用测量。
