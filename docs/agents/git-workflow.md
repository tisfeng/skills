# Git 工作流

本文规定本仓库的 Git 授权和交付要求；请求语义、Mutation Gate 和 protected 以
[`request-boundary.md`](request-boundary.md) 为准，plan/history 生命周期以
[`README.md`](README.md) 为准。

## 基本安全

- 保留用户现有 staged、unstaged 和 untracked 内容，不重写或丢弃无关工作树状态。
- implementation 默认候选自动本地提交；明确禁止提交、仅预览或暂缓交付时不得暂存或提交。
- 自动本地提交不授权 push、pull、rebase、merge、创建分支、发布或强制移动 ref。
- 每个提交聚焦一个连贯变更，使用 Angular-style 信息，并遵循实际加载的 `git-commit` Skill。

## Git 交付顺序

1. 完成必要审查和验证，等待其他写入 Agent 结束。implementation 自动交付仅包含允许范围内
   的本任务变更和同任务 history；显式交付按用户获准范围及所选模式，不反向要求补写 history。
2. 当前主 Agent 串行完成 Git 交付：提交使用 `git-commit`，集成使用 `worktree-rebase-merge`。
   提供当前用户限制、获准范围和已有的任务初始状态、内容归属及验证证据；保留上下文中的真实
   记录即可，不要求项目规则采用 Skill 内部的变量名或数据格式。
3. 读取实际加载的 Skill，由它完成必要预检、执行、结果校验和回执。Skill 缺失或无法安全交付
   时报告具体缺口；不通过修改项目规则补偿 Skill 缺陷，也不扩大已有授权。

## 自动本地提交条件

以下条件必须同时满足：

- 任务是 `implementation`，`delivery_authorization=auto-local-commit`，且没有仍有效的禁止、确认
  或暂缓交付要求；
- Agent 产生仓库文件差异，并创建或更新同任务 history；
- 提交范围只包含获准且归本任务所有的变更；
- 必要审查与验证覆盖最终内容，没有未处理的阻塞 finding、验证失败或证据缺口；
- `git-commit` 的自动提交安全检查通过，包括任务初始状态和内容归属证据充分。

自动提交只精确暂存本任务变更，不使用 `git add .`。显式交付遵循所选工作流，不反向套用
implementation 的 history 或自动提交资格；未满足自动提交条件不否决已有的 staged-only 授权。

条件不满足时保留现场，报告受阻操作和原因；可以继续范围内的实施、修复与复验。不能因为用户
没有再次说“提交”，就把有效的 `auto-local-commit` 降级为未提交。
