# review-pr 复用已关联的同名分支

- 日期：2026-10-27
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-10/2026-10-27-review-pr-linked-branch-reuse.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

按准确 Git upstream 复用 PR 同名分支，不因作者身份或 remote 别名重复创建 review 分支；无同名分支时创建并关联。

## 实际变更

- helper 用 upstream 的实际仓库地址和远程分支识别关联，首次准备、复审及既有干净 worktree 均支持跨作者复用。
- 已关联分支落后时仅快进，领先时保留本地提交并审查冻结远程对象，分叉或领先状态下请求 latest-base 时停止。
- 保留原 remote 别名、本人无 upstream 分支补关联的行为及未关联冲突分支的既有处理；新建分支自动 tracking 的结果有回归测试覆盖。
- 新增准确的 linked_pr_branch_reused 回执，保持 self_authored 字段原义；显式复用旧 fallback 分支不误报同名关联分支复用。
- 更新技能入口、本地准备协议、报告说明及现有测试，未新增独立关联存储或改动命名技能。

## 验证

- review-pr 全套 77 项测试通过，其中分支准备 34 项；消费者可移植性 3 项通过。
- 技能校验（6 个技能及发现入口）、quick_validate、Python 编译、Shell 语法及 diff 检查通过。
- 按 review 技能审查完整任务差异，无未解决 finding；最终技能快照 SHA-256 已复验。
- 使用临时本地 Git 仓库和 fake gh 验证，未访问真实 PR 进行准备或评论操作；不声称真实 GitHub 交互已验证。

## 交付

- 当前 main 分支本地提交技能、测试、本记录和归档计划，不 push、不发布、不更新全局或消费方技能。
