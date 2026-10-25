# review-pr 先回复再关闭线程

- 日期：2026-10-25
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-10/2026-10-25-review-pr-reply-resolve.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

明确调用 review-pr 时逐条检查开放线程，确认已修复或不再适用后，回复依据再关闭。

## 实际变更

- 入口明确默认评论维护与只读限制，保留对全部评论、回复和准确远程代码的检查；outdated 不能直接作为关闭依据。
- 线程 helper 的 version 2 plan 必须包含回复正文；apply 同时要求回复与 resolve 开关，旧 plan 需重新生成。
- 先发布回复并确认状态及完整线程，再 resolve；回复和关闭分别记录结果，部分失败返回非零退出码。
- 重新复核并生成新 plan 后，复用当前登录用户已经发布且正文完全一致的回复；不复用待发布回复或其他人的回复。
- 依据 [GitHub GraphQL 线程 API](https://docs.github.com/en/graphql/reference/pulls#addpullrequestreviewthreadreply) 接入回复；gh 字符串参数按原文传递。
- 更新 fake API 测试、报告协议及示例，记录回复链接、回复数、关闭数、开放状态与失败原因。

## 验证

- review-pr 全套 68 项测试通过；最终源码快照直接相关的 39 项测试通过，其中线程测试 18 项。
- 消费者可移植性 3 项测试通过；技能校验（6 个技能及发现入口）、quick_validate、Python 编译与 diff 检查通过。
- 按 review 技能审查完整任务差异，修复已发布状态检查和 gh 字符串参数问题后复验，无未解决 finding。
- 使用 fake API，未操作真实 PR；尚未验证 GitHub 实际发布与关闭行为，不将静态及模拟验证当作线上验证。

## 交付

- 在当前 main 分支创建本地提交，包含技能修改、测试、本记录及归档计划。
- 不 push、不发布、不更新全局或消费方安装。
