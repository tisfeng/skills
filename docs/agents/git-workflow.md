# Git 工作流

本文只规定 Git 状态保护、暂存和本地交付；请求语义、Mutation Gate 和 protected 以
[`request-boundary.md`](request-boundary.md) 为准，plan/history 生命周期以
[`README.md`](README.md) 为准。

## 基本安全

- 保留用户现有 staged、unstaged 和 untracked 内容，不重写或丢弃无关工作树状态。
- implementation 默认候选自动本地提交；明确禁止提交、仅预览或暂缓交付时不得暂存或提交。
- 自动本地提交不授权 push、pull、rebase、merge、创建分支、发布或强制移动 ref。
- 每个提交聚焦一个连贯变更，使用 Angular-style 信息，并遵循实际加载的 `git-commit` Skill。

## Git 交付顺序

1. implementation 使用首次写入前冻结的 HEAD、索引、工作树、冲突、允许路径和内容归属判断
   交付安全；只读开始的显式 staged 交付或复用已有提交的 integration，在准备交付时建立同等内容
   的只读基线。
2. 完成最终审查和验证后按操作冻结交付范围。自动交付时，`expected_commit_paths` 逐一列出本任务
   实际产生且归 Agent 所有的每个改动路径，不遗漏、不混入用户原有内容，且全部属于
   `task_allowed_paths`。自动提交资格失败不能用于否决用户明确授权的 staged-only 提交。
3. 所有实现和其他写入 Agent 完成后，主 Agent 冻结 `agent_owned_paths`、`expected_commit_paths`
   和最终验证结果，再串行调用 `git-delivery`。
4. `commit` 与 `auto-local-commit` 操作使用实际加载的 `git-commit` Skill；`integration` 操作使用
   实际加载的 `worktree-rebase-merge` Skill。找不到所需 Skill 时 fail closed，不改用缩减流程。
5. 需要创建提交时先执行只读 `prepare`，在主对话展示提交信息预览，再由同一交付 Agent 执行
   `apply`。普通预览不是新的确认门槛；只有用户要求确认、仅预览或暂缓时才等待批准。

## 通用 Git 交付子代理

`.codex/agents/git-delivery.toml` 是本仓库发布的通用本地 Git 交付角色。它只消费主 Agent 已确认的
授权、operation、phase、初始快照、允许路径和 `staging_strategy`，不修改产品内容，也不自行决定宿主
仓库是否默认提交。

- 已有 staged 内容的显式 `commit` 使用 `existing-index`：`prepare` 只冻结 staged paths 与 staged raw
  patch；`apply` 只复验该 patch，绝不运行 `git add`，同路径未暂存内容不能进入提交。
- 空索引且允许暂存：`prepare` 冻结 `staging_strategy`、候选路径、未暂存 raw patch、任务相关未跟踪
  内容摘要和草稿；`apply` 将该策略作为执行 `git-commit` Skill 的同一个唯一暂存步骤，不能由子代理和
  Skill 重复暂存。显式、未限定范围的 `commit` 或 `integration` 可使用 `explicit-worktree-once`；
  显式路径范围使用 `explicit-paths`；自动本地提交只能使用 `auto-exact`。
- `explicit-worktree-once` 的 staged paths 与 raw patch 必须完全等于冻结的全工作树候选；
  `explicit-paths` 与 `auto-exact` 的预期暂存集合必须属于 `task_allowed_paths`，允许范围较宽时不得要求
  未修改路径也进入 staged。
- `commit` 和 `auto-local-commit` 只执行 `git-commit`；只有 `integration` 授权才允许执行
  `worktree-rebase-merge` 明示的分支、rebase、merge 或临时 worktree 操作。
- `integration` 复用既有源提交且无需创建新提交时，只冻结和复验提交范围，不要求提交信息预览。
- 配置、授权、模型、范围、HEAD、索引、冲突、目标 worktree 或验证不确定时进入 protected。
- 若本轮正在更新 `git-delivery` 配置且运行时尚不能重新发现它，只可按 TOML 中完全相同的模型、
  推理强度、权限和指令启动 bootstrap fallback；无法精确复现时 fail closed。
- 完成后主 Agent 独立核验提交哈希、实际信息、分支、最终工作树和未 push 状态。

## 自动本地提交条件

以下条件必须同时满足：

- 任务是 `implementation`，`delivery_authorization=auto-local-commit`，且没有仍有效的禁止、确认
  或暂缓交付要求；
- 初始索引为空，任务期间没有新增非 Agent staged 内容；
- `initial_head` 未变化，当前索引无冲突，用户内容与 Agent 变更可以清晰分离；
- Agent 产生仓库文件差异，并创建或更新同任务 history；
- `task_allowed_paths`、`agent_owned_paths` 和 `expected_commit_paths` 已明确；
- 最终 staged paths 与 `expected_commit_paths` 完全相等，且后者属于 `task_allowed_paths`；
- 必要审查与验证覆盖最终内容，没有未处理的阻塞 finding、验证失败或证据缺口；
- 当前任务尚未执行过自动提交。

自动提交只暂存 `expected_commit_paths`，绝不使用 `git add .`。没有仓库差异时不创建空提交。
显式交付遵循所选工作流，不反向套用 implementation 的 history 或初始空索引前提。

条件不满足时保留现场，报告受阻操作和原因；可以继续范围内的实施、修复与复验。不能因为用户
没有再次说“提交”，就把有效的 `auto-local-commit` 降级为未提交。
