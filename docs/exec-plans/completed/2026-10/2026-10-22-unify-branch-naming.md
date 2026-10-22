# 统一分支命名规则与消费端

- 状态：completed
- 创建日期：2026-10-22
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

分支命名规则散落在多个技能文档和脚本中，PR 分支约定被误用于普通本地提交。

## 目标与范围

- 目标结果：以 git-commit 为唯一命名来源，消费技能调用统一工具；同步 Easydict 并明确 PR 规则边界。
- 允许修改路径：skills 仓库的相关技能、验证测试与任务文档；Easydict 的受管技能、lock、AGENTS.md、CONTRIBUTING.md、发布技能及任务文档。
- 同任务 history：`docs/histories/2026-10/2026-10-22-unify-branch-naming.md`
- 用户限制：不创建或切换分支；验证后本地提交；不 push。允许调整相关测试并补充必要的命名验证。
- 非目标：创建 PR、发布版本、变更 Git 集成策略或重命名已有分支。
- 验收标准：任务、审查和发布分支使用同一规则；保留显式名称与现有分支；消费者可移植性验证通过。

## 工作计划

1. 实现统一命名规范、只读工具和消费端引用，补充并运行相关测试。
2. 审查差异、记录 history 并创建本地提交。
3. 后续 Easydict 同步由消费仓库同名计划单独跟踪。

## 风险与决策

- 命名依赖通过完整 git-commit 技能提供，依赖缺失时明确失败；不保留第二套正则。
- 保留用户明确名称和既有非标准分支；命名工具不操作 Git 分支。
- 本地同步以准确上游提交为证据，不伪称远程发布版本。

## 进度

- [x] 上游实现、相关测试和审查完成，准备本地交付。
- [x] 下游交付范围由 Easydict 同名计划跟踪。

## 验证

- `python3.12 scripts/validate-skills.py`：6 个技能校验通过。
- 单测：git-commit 25、submit-pr 29、review-pr 64、worktree-rebase-merge 6、portability 3、validator 2，共 129 项通过；最终 Shell 整理后另复跑 PR 准备测试。
- `python3.12 -m compileall -q scripts skills`、`bash -n`、`git diff --check`：通过。
- Review：基线 `526932ffc4ae9a79304e416c71c147c911295723`，检查共享工具、消费端调用、依赖指纹、命名与显式名称边界；未发现有效 finding。

## 完成条件

- 上游必要验证通过，差异审查完成，plan/history 完整，本地提交且无 push；消费仓库独立完成后续同步。
