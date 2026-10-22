# 统一分支命名规则与消费端

- 日期：2026-10-22
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-10/2026-10-22-unify-branch-naming.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

以 git-commit 为唯一分支命名来源，统一任务、审查与发布同步命名，消除各消费者的重复规则。
用户要求保留当前分支、本地提交且不 push，并明确允许相关测试修改。

## 实际变更

- git-commit 提供统一规范及只读 `branch_name.py`，支持生成、分类、字面校验和冲突候选。
- submit-pr 和 worktree-rebase-merge 加载同级命名工具；review-pr 调用统一 CLI，并将共享工具纳入依赖指纹。
- 统一保留用户明确名称和既有分支，Agent 自动拟名禁止身份前缀；PR 保护策略仍归 PR 工作流维护。
- 更新依赖文档、README、命名单测和隔离消费测试；依赖缺失时明确失败，不复制第二套规则。
- Easydict 的安装、lock 与发布消费端由消费仓库同名任务记录。

## 验证

- 技能校验：6 个公开技能及发现入口通过。
- git-commit 25、submit-pr 29、review-pr 64、worktree-rebase-merge 6、portability 3、validator 2，共 129 项单测通过。
- 最终 Shell 整理后另复跑 PR 准备 28 项和隔离消费 3 项，均通过。
- Python 编译、Shell 语法和 diff 空白检查通过。
- Review：以首次写入前 HEAD 为基线，检查完整差异、缺失依赖、显式名称、PR head 保护和读取路径；无有效 finding。

## 交付

- 在原 main 分支创建本地提交，不创建或切换分支，不 push、不创建 PR、不发布版本。
