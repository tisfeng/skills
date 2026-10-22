# 修复分支命名审查问题

- 日期：2026-10-22
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-10/2026-10-22-fix-branch-review.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

修复共享命名依赖预检遗漏及本地复用分支校验未统一两个 finding；用户要求保留当前分支，本地提交，不 push、不发布。

## 实际变更

- submit-pr 在分支预检入口加载命名依赖，不再等到 fetch 后才发现依赖缺失。
- review-pr 的本地 reuse-branch 校验调用统一工具，保留远程 PR head/base 的完整 ref 协议。
- 扩展隔离消费者缺失依赖测试覆盖 preflight/plan，并验证 refs、索引和工作树不变。
- 新增 apply 不进入 fetch 的回归检查，扩展非法本地名称用例覆盖 HEAD、前导连字符和 checkout 简写。
- 不将未发布修复同步到 Easydict；下游恢复固定版本由该仓库单独记录。

## 验证

- submit-pr 30、review-pr 64、隔离消费 3，共 97 项测试通过。
- 6 个技能及发现入口校验、Python 编译、Shell 语法、diff 空白检查通过。
- Review：对照首次写入前 HEAD 检查完整差异，两个 finding 已解决，无新增有效 finding。

## 交付

- 原 main 分支本地提交；不创建或切换分支，不 push、不发布。
