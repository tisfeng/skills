# 本人 PR 审查复用功能分支

- 状态：completed
- 创建日期：2026-09-27
- 负责人：Codex
- 关联 Issue/PR：tisfeng/Easydict#1332（问题证据）

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 背景

本人提交 PR 后继续产生本地提交，准备 helper 将本地领先判为冲突并新建 review 分支。
用户要求保留功能分支，仍按远程 PR 的准确 SHA 审查。

## 目标与范围

- 目标结果：复用本人 PR 同名分支，区分 checkout 与远程审查快照。
- 允许修改路径：`skills/review-pr/`，本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-27-reuse-self-authored-pr-branch.md`
- 用户限制：执行已批准方案，包含对应回归测试；只在 skills 仓库本地交付。
- 非目标：修改消费方安装、切换 Easydict 分支、push、创建 PR、发布和清理既有 review 分支。
- 验收标准：领先分支与提交保留，无新增 review 分支；同 SHA、快进、复验、已占用 worktree、
  分叉及错误 upstream 均有明确结果；远程源码与验证证据不混用本地领先内容。

## 工作计划

1. 调整 helper 分支选择、已有 worktree 复用、SHA 复验和结构化回执。
2. 同步技能入口、本地准备、取证、报告协议与回归测试。
3. 运行相关单测、资产校验、可移植性验证，使用 review 审查最终差异。
4. 更新 history，归档计划并按 git-commit 创建本地提交。

## 风险与决策

- 本地 HEAD 可能不同于远程 SHA；准备回执升级版本，明确只从冻结 Git 对象取证。
- latest-base 模式仍要求准确 PR head，领先时停止，避免把本地额外提交混入集成结果。
- 本人分支身份冲突或分叉时停止；复用已有 worktree 时验证目标干净并保留调用 checkout。
- 初始 HEAD 为 `64bc691b015b9d7a9b3c119a7f0be2523d22ed64`，初始工作区和索引干净。

## 进度

- [x] 实现与文档。
- [x] 验证与审查。
- [x] history、归档及本地提交准备。

## 验证

- 分支准备单测首轮 28 项通过，覆盖本地领先、复验、已有 worktree、错误 upstream、分叉及远程 Git 对象取证。
- 可移植性测试 2 项通过；Skill 资产校验、quick_validate、Shell 语法、Python 编译与差异空白检查通过。
- 使用 review 检查实现、完整差异和调用协议，未发现需要修复的有效 finding；回执升级版本防止旧调用者误认为 checkout 必须等于远程 head。
- 补齐普通/集成回执断言及命令行说明后，最终分支准备单测 28 项通过（63.730 秒）。

## 完成条件

- 范围内实现和验证通过，无未解决的有效审查问题。
- history 记录最终行为与证据，计划归档，本地提交校验通过。
