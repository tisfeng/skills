# 发布 Skills v0.8.1 并更新 Easydict

- 日期：2026-10-23
- 状态：completed
- 关联计划：[发布与升级计划](../../exec-plans/completed/2026-10/2026-10-23-release-and-upgrade-easydict-v0.8.1.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

发布 skills 新版本，再按正常流程更新 Easydict 的受管副本。不创建或切换分支。

## 实际变更

- 发布 v0.8.1 补丁版本，公开内容仅调整 submit-pr 的标题和正文语言契约。
- 新增版本 changelog，按完整版本范围提炼单条更新；正文仍以 tag 内 changelog 为唯一来源。
- 完成固定 tag 的隔离安装后，通过 skills@1.5.25 更新 Easydict 的六个受管 Skill、lock 和来源基线。
- 不修改产品代码、项目专属或第三方技能，不全局安装；Easydict 只创建本地提交。

## 验证

- 完整矩阵 137 项通过：git-commit 25、worktree-rebase-merge 6、review-pr 64、review 7、共享契约 5、submit-pr 30。Skill 结构、Python 编译、Shell 语法、空白检查、changelog 和记录文件名均通过。
- 发布提交 `1b40de2c4a1b03dcc117b14a1d089d3445bb2b9c` 已推送 main；同 SHA 的[代码 CI](https://github.com/tisfeng/skills/actions/runs/39813451441)及[文档 CI](https://github.com/tisfeng/skills/actions/runs/39813451546)成功。
- annotated tag v0.8.1：tag object `d033324dd8e3b882ad8694836693df5dfd5e12a6`，peeled commit 与发布 SHA 一致，本地和远程已核验。
- [Release v0.8.1](https://github.com/tisfeng/skills/releases/tag/v0.8.1) 发布于 2026-10-22T16:24:06Z，非 draft、非 prerelease；标题精确为 v0.8.1，正文与 tag 内 changelog 全文一致。
- [Release workflow](https://github.com/tisfeng/skills/actions/runs/39813693889) 成功；skills@1.5.25 从固定远程 tag 隔离安装六个完整技能，56 个文件逐一匹配 archive，目录 hash 和 lock 一致，已安装 CLI 冒烟检查通过。
- Easydict 通过同版本安装器同步六个受管技能，56 个文件和目录 hash 匹配，submit-pr 现有 30 项测试通过；项目专属和第三方 Skill、第三方 lock 条目及符号链接未变。
- Easydict 本地提交 `9aa0a6a90c6f75db4ebb8de507cb502e19491a52`，分支 dev，工作树干净，未 push。
- 本任务仅新增发布文档及同步已验证的文档快照，无生产脚本变更；版本范围与安装增量均已核对，无需独立代码 Review。

## 交付

- skills/main 与 annotated tag 已推送；计划已归档，真实验收证据随发布记录提交推送，不移动公开 tag。
- Easydict/dev 已完成本地升级提交，未推送或创建 PR。
- 两个仓库保持原分支；最终内容和保护资产已核对。
