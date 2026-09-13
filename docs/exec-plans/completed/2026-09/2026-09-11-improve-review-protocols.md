# 改进 review 与 review-pr 执行协议

- 状态：completed
- 授权：用户批准上一轮方案的前两批实施；不操作真实 PR、不 push、不发布或更新全局安装。
- 初始 HEAD：`053509d8a4b4efcf3673482630490df2fee8b1e0`
- 分支：`codex/perf-local-review-latency`
- 初始 staged / unstaged / untracked：均为空，无冲突。
- 交付：按仓库规则自动精确本地提交，不修改 main。
- 独立规划：复用上一轮 Planner 结论；目标、范围、脚本和风险假设未变化。

## 范围与完成条件

允许路径及 Agent-owned 范围为 `skills/review/`、`skills/review-pr/`、本执行计划和同任务
`docs/histories/2026-09/2026-09-11-improve-review-protocols.md`。保留其他并发修改。

1. PR 验证使用冻结范围，base 漂移驱动明确的范围复验；复用本地 range 取证。
2. 准备脚本提供 expected-head 守卫和结构化回执，消除同轮重复 head/base fetch。
3. 大 PR 提供可选的完整证据分页与变化线程传输；完整远程读取和最终刷新不变。
4. resolve 前后定向读取 PR 身份和目标线程全部回复，保留权限、漂移和结果读回守卫。
5. 同步技能和参考说明、行为测试；独立审查后归档计划与 history。

本地 diff 缓存不在本轮实施范围：现有测量尚不能证明值得引入。保持所有既有模式、完整报告、
逐命令权限、只读限制和 CI 默认不等待；不通过删减技能篇幅或检查提速。

## 验证与风险

- 使用临时 Git 仓库、fake gh / GraphQL；禁止测试真实 PR mutation。
- 覆盖干净 checkout 的已提交空白错误、head/base 漂移、fetch 次数、冲突与 worktree 保护。
- 覆盖证据缺页/截断/损坏、线程新增删除与回复变化、指纹稳定性、resolve 部分失败。
- 运行两个技能相关 Python 测试、Skill 校验、Python 编译、Shell 语法和 diff 检查。
- 由独立 reviewer 审查最终生产实现、测试和协议一致性；测试证据绑定最终内容。
- 性能以请求次数、回传数据量和隔离基准验证；不把 helper 耗时等同真实 Agent 端到端提速。

## 进度

- [x] 写入前检查及独立规划复用
- [x] 实现与文档同步
- [x] 行为验证、独立审查及修正
- [x] history、归档与精确本地交付准备（提交身份以 Git 回执为准）

## 验证结果

- PR 行为测试 67 项通过，本地 review 测试 10 项通过；加强同一组回复仅顺序变化的断言后，
  对应快照测试 17 项增量复验通过。
- Skill 仓库校验、两个 Skill 的 quick_validate、Python compileall、Shell 语法和 diff 检查通过。
- 独立 reviewer 对最终生产实现、协议和测试未发现需修复的 P0–P3 finding；生产文件哈希复验一致。
- 200 线程、1 线程变化的模拟刷新：全量 627876 字节，差量 31937 字节，减少 94.9%。
- 未测试真实 PR mutation、真实网络下的 Agent 端到端提速；没有 push、发布或更新全局技能。
