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

1. implementation 使用首次写入前记录的 HEAD、索引、工作树、冲突、允许路径和内容归属判断
   交付安全；显式 staged 交付或复用已有提交的集成，在准备交付时建立相应的只读基线。
2. 完成必要审查和验证，等待其他写入 Agent 结束，再冻结实际交付范围。自动提交的
   `expected_commit_paths` 必须逐一包含本任务实际产生且归 Agent 所有的改动路径，并全部属于
   `task_allowed_paths`。自动提交资格失败不能用于否决用户明确授权的 staged-only 提交。
3. 当前主 Agent 直接、串行执行 Git 操作：提交使用 `git-commit`，集成使用
   `worktree-rebase-merge`。执行前读取实际 Skill；找不到时报告缺失并停止相关操作。
   暂存策略、候选内容复验和唯一暂存步骤以 `git-commit` 为准。
4. 新提交遵循 `git-commit` 的 **先确定模式** 和 **提交与可见预览**；复用已有提交无需重新起草信息。
5. 写入前复验相关 HEAD、索引、工作树和范围，发生非预期变化时保留现场并停止相关操作。
   已知 Git 写入位置受限时，直接为已授权命令申请必要提权，避免重复尝试必然失败的命令。
6. 按 Skill 核验提交和集成结果，并呈现完整回执。实际提交信息直接读取 Git，不重新起草或
   翻译；保留完整哈希、校验结果、分支、工作树、push 状态及统计表。

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
