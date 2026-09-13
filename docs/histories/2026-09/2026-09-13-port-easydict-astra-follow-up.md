# 参考 Easydict 精简 Agent 规则

- 日期：2026-09-13
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09/2026-09-13-port-easydict-astra-follow-up.md)

## 目标

参考 Easydict 2026-09-13 的 Agent 文档精简提交，让当前仓库的宿主文档只保留项目特有
规则，通用 Git、review 和 Skill 执行契约交由对应 Skill 维护。

## 实际变更

- 将根 `AGENTS.md` 收窄为任务模式和四个项目专属路由，保留自动本地提交和外部写入
  授权边界，删除通用 Review、Skill 调用和交付说明。
- 删除与 `git-commit`、`review-pr` 和 `worktree-rebase-merge` 重复的
  `docs/agents/request-boundary.md` 与 `docs/agents/git-delivery.md`。
- 将文档生命周期、宿主/Skill 职责和公开源码/发现链接边界收敛到 `docs/agents/README.md`；
  删除重复的 `docs/design-docs/overview.md`，并保留 `docs/design-docs/README.md` 说明目录职责。
- 补齐 `docs/exec-plans/README.md` 与 `docs/histories/README.md`，链接继续保留的计划模板和
  history 模板，不建立第二套规则入口。
- 恢复本仓库任务使用当前 checkout Skill 源码的规则；同名全局版本并存时要求核对实际加载
  路径。Skill 验证范围统一由 `docs/agents/build-and-test.md` 维护。
- 执行计划模板只保留背景、目标范围、工作计划、风险、进度、验证和完成条件，删除运行时
  状态、授权字段和 Git 快照样板。
- 合并验证证据复用的重复说明，删除开发规则中已由根入口覆盖的语言规则。
- 将 42 份 completed plan 按创建月份迁入 `docs/exec-plans/completed/2026-09/`，同步修正
  42 处 history 链接，并让现行规则与模板明确使用 `completed/YYYY-MM/`。
- `skills/`、`docs/release/` 和 history 模板保持不变；Easydict 的 Xcode、SFSafeSymbols、受管
  lock、Release Skill 和 Claude 配置未移植。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，验证 6 个公开 Skill 及仓库发现入口。
- 活动文档的删除路径、旧状态字段、相对链接和核心边界检查：通过。
- completed 根目录 Markdown 数量为 0，`2026-09/` 内为 42；目录月份均与文件日期一致。
- 旧 completed 文件路径引用为 0；42 处新路径链接的目标均存在。
- design doc、exec plan 和 history 的目录 README 均存在，计划与 history 模板均保留，声明的
  相对链接目标存在。
- 6 个项目 Skill 发现链接均解析到当前 checkout；6 个同名全局 Skill 均与当前源码不同。
- `git diff --check` 与本任务 Markdown 尾随空白检查：通过。
- 根入口与现行专题规则保持精简；目录 README 只说明结构并指向现行权威来源。
- 构建和运行时测试：未运行；本任务只修改治理 Markdown，不修改 Skill、脚本或运行时代码。

## 交付

用户在内容验证后显式调用 `worktree-rebase-merge`，授权本地分支、暂存、提交、rebase 与
merge；未授权 fetch、pull、push 或发布。
