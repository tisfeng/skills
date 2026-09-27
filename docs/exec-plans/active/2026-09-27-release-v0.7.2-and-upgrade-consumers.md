# 发布 Skills v0.7.2 并升级消费者

- 状态：active
- 创建日期：2026-09-27
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-5`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 背景

`tisfeng/skills` 在 v0.7.1 后新增了 `review-pr` 报告生成时机、报告组合规则和交付检查改进；三个消费者仍固定使用 v0.7.0，需要先发布 v0.7.2，再同步固定 tag。

## 目标与范围

- 目标结果：发布 v0.7.2，并将 Easydict、Scoco、issues-translate-action 的六个受管 Skill 更新到 v0.7.2。
- 允许修改路径：本仓库版本 changelog、plan/history；三个消费者的六个受管 Skill、lock、来源/通知文档及 plan/history。
- 同任务 history：`docs/histories/2026-09/2026-09-27-release-v0.7.2-and-upgrade-consumers.md`
- 用户限制：Raycast-Easydict 和 SelectedTextKit 不在范围；保留独立第三方 Skill、项目专属 Skill、产品代码和运行时资产。
- 非目标：不修改其他依赖、不重写消费者现有分支历史；除发布仓库明确发布步骤外不创建消费者 PR。
- 验收标准：v0.7.2 tag/Release 与 changelog 一致；三个消费者 lock、目录快照和来源说明固定到 v0.7.2；各仓库本地提交完成。

## 工作计划

1. 创建 v0.7.2 changelog，验证发布范围并创建发布提交。
2. 推送发布提交，创建 annotated tag，等待 workflow 创建并验收 GitHub Release。
3. 使用固定安装器同步三个消费者的六个受管 Skill，更新 lock 和来源说明。
4. 运行验证、review，归档各仓库 plan/history 并创建本地消费者提交。

## 风险与决策

- 使用稳定的 annotated tag，不同步未发布分支或手工修改 computed hash。
- 消费者保留当前分支和既有未相关提交；Raycast-Easydict、SelectedTextKit 明确跳过。
- 发布仓库的 push、tag 和 GitHub Release 仅针对 v0.7.2，失败时按发布流程停止并保留证据。

## 进度

- [ ] 创建 changelog 与发布提交。
- [ ] 推送 main、创建 tag 并验收 Release。
- [ ] 同步三个消费者并验证快照。
- [ ] 创建消费者本地提交并归档记录。

## 验证

- 发布仓库运行结构校验、Python 编译、Shell 检查和相关 Skill 测试。
- 发布后核对 tag peeled SHA、Release 标题/正文和固定 tag 隔离安装。
- 消费者逐文件比较六个 Skill 与 v0.7.2 tag，重算目录 hash、运行受管 Skill 测试和 `git diff --check`。

## 完成条件

- v0.7.2 的 main 提交、annotated tag、GitHub Release 和隔离安装验收完成。
- 三个消费者完成 v0.7.2 快照更新并各自创建本地提交。
- plan 归档、history 记录真实证据；Raycast-Easydict 和 SelectedTextKit 未修改。
