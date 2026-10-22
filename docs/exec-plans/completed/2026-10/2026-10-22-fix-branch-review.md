# 修复命名审查问题

- 状态：completed
- 创建日期：2026-10-22
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

统一命名工具新增后，submit-pr 预检漏查必需依赖，review-pr 的本地复用分支校验仍使用旧路径。

## 目标与范围

- 目标结果：依赖缺失时在 Git 写入前失败，本地复用名称经过共享工具校验。
- 允许修改路径：相关 submit-pr/review-pr 脚本、测试、隔离消费者测试及本任务文档。
- 同任务 history：`docs/histories/2026-10/2026-10-22-fix-branch-review.md`
- 用户限制：保持原 main 分支；不创建或切换分支；验证后本地提交，不 push、不发布。沿用本任务已获准的相关测试修改。
- 非目标：改变命名格式、远程 PR ref 协议或更新消费仓库技能。
- 验收标准：缺少依赖的 preflight/plan 均失败，apply 不进入 fetch；本地名称拒绝 HEAD、前导连字符及非法 ref。

## 工作计划

1. 修复预检和本地名称校验路径，更新针对性回归测试。
2. 执行相关验证和 review，记录结果、归档计划并本地提交。

## 风险与决策

- 远程 PR head/base 的完整 ref 校验保持原协议，只统一本地分支字面名校验。
- Easydict 恢复已发布固定版本，不同步本次未发布上游修复。

## 进度

- [x] 实现和验证。
- [x] Review、记录与本地提交。

## 验证

- submit-pr 30、review-pr 64、隔离消费 3，共 97 项测试通过。
- 技能发现校验（6 个技能）、Python 编译、Shell 语法、`git diff --check`：通过。
- Review：基线 `03ae792c938972bedcbaba3f7d72fd4c03f34e87`，核对必需依赖在 fetch 前检查、本地字面校验接入和远程 ref 协议保留，两个 finding 均已修复，未发现新问题。

## 完成条件

- 必要验证和审查通过，本地提交完成，无 push 或发布。
