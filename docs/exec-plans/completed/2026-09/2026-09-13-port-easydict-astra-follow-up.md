# 参考 Easydict 精简 Agent 规则

- 状态：completed
- 创建日期：2026-09-13
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

上一轮已将 Easydict 提交 `f19ec3b8890dfa43d40454f524ca1807b6c945cc` 的任务模式收回根
入口，但未提交。用户进一步要求参考 Easydict 2026-09-13 的 Agent 治理提交继续
精简，并已批准执行前一轮给出的方案。

## 目标与范围

- 目标结果：宿主文档只保留本项目特有规则，通用 Git、review 和 Skill 执行契约由对应
  Skill 维护。
- 允许修改路径：`AGENTS.md`、`docs/agents/`、`docs/design-docs/`、
  `docs/exec-plans/`、`docs/histories/`。
- 同任务 history：`docs/histories/2026-09/2026-09-13-port-easydict-astra-follow-up.md`
- 用户后续显式调用 `worktree-rebase-merge`，授权本地分支、暂存、提交、rebase 与 merge；
  不 fetch、pull、push 或发布。
- 非目标：不修改 `skills/`、测试、history 模板、`docs/release/`、版本或 CI；不移植
  Easydict 的 Xcode、SFSafeSymbols、受管 lock 或 Claude 配置。
- 验收标准：自动本地提交、history、外部写入、发布和公开 Skill 资产边界均保留；
  当前 checkout 的 Skill 源码优先级明确；文档目录 README 与模板齐全；completed plan 按月
  归档且引用有效；活动文档无被删规则的引用；静态检查通过。

## 初始状态

- 初始 HEAD：`24de6e8b8efc23f63131c5160cd3145b6a62898c`（detached）。
- 初始 staged 路径：none；初始冲突：none。
- 初始 unstaged：`AGENTS.md`、`docs/agents/request-boundary.md`、
  `docs/design-docs/overview.md`。
- 初始 untracked：本计划的已归档版本与同任务 history。
- 内容归属：上述差异均由上一轮同任务产生，本轮在其上继续收敛。
- 交付授权：integration；以用户后续显式调用 `worktree-rebase-merge` 为准。

## 工作计划

1. 精简根任务模式和项目路由，保留自动本地提交与外部写入边界。
2. 删除重复的 `request-boundary.md`、`git-delivery.md` 和 Agent 资产设计概览，将唯一有效的
   项目边界收回 `docs/agents/README.md`。
3. 压缩治理文档与执行计划模板，只对验证和开发规则做已确认的小幅去重。
4. 将 completed plan 按 `YYYY-MM` 目录归档，并同步仓库内链接与现行规则。
5. 补齐 design doc、exec plan 和 history 的目录 README，保留并链接现有模板。
6. 恢复当前 checkout Skill 选择规则，让验证范围继续由构建与测试文档统一维护。
7. 更新本计划与 history，检查删除路径、相对链接、关键规则和最终差异。

## 风险与决策

- Mutation Gate、protected 状态和 Git 暂存细节从宿主文档删除，但不改写现有
  `git-commit`、`review-pr` 或 `worktree-rebase-merge` 的安全契约。
- 设计概览的非显然内容先合并到治理文档，再删除重复文件。
- `docs/design-docs/overview.md` 继续删除；目录用途由 README 说明，不恢复重复设计概览。
- 按计划文件名中的日期确定归档月份；当前 42 份 completed plan 均归入 `2026-09/`，同步
  修正 42 处历史链接，不改写记录的历史事实。

## 进度

- [x] 完成当前规则、Easydict 当日提交和现有差异的只读比较。
- [x] 完成宿主规则与计划模板精简。
- [x] 完成 42 份 completed plan 的月度归档与历史链接迁移。
- [x] 补齐三个文档目录 README，确认计划与 history 模板继续保留。
- [x] 恢复当前 checkout Skill 选择规则并消除验证范围重复定义。
- [x] 完成 history、静态验证和计划归档。

## 验证

- 活动文档的被删路径、Mutation Gate、protected 和旧模板字段检索：无残留。
- 本次变更的 Markdown 相对链接和核心边界检查：通过。
- completed 根目录 Markdown 数量为 0，`2026-09/` 内为 42，目录月份与文件日期一致。
- 旧 completed 文件路径引用为 0；42 处新路径链接的目标均存在。
- `docs/design-docs/`、`docs/exec-plans/` 和 `docs/histories/` 的 README 均存在，计划与
  history 模板均保留，声明的相对链接目标存在。
- 6 个项目 Skill 发现链接均解析到当前 checkout；6 个同名全局 Skill 均与当前源码不同。
- `python3.12 scripts/validate-skills.py`：通过，验证 6 个公开 Skill 及仓库发现入口。
- `git diff --check` 与本任务 Markdown 尾随空白检查：通过。
- 构建和运行时测试：未运行；本任务只修改治理 Markdown。

## 完成条件

- [x] 根入口和专题文档不再重复通用 Skill 契约。
- [x] 自动本地提交、history、外部写入、发布与 Skill 源码边界仍可直接定位。
- [x] 目录 README 和模板齐全，且不恢复重复的设计概览。
- [x] 本仓库任务明确使用当前 checkout 的 Skill 源码。
- [x] completed plan 使用 `YYYY-MM` 月度目录，仓库内链接均指向新路径。
- [x] 最终内容的链接、规则语义、Skill 发现校验和 `git diff --check` 通过。
