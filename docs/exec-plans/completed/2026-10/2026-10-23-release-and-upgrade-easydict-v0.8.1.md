# 发布 Skills v0.8.1 并更新 Easydict

- 状态：completed
- 创建日期：2026-10-23
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

submit-pr 已将标题语言与正文语言分离。用户要求发布新版本，再按正常流程更新 Easydict。

## 目标与范围

- 目标结果：发布 v0.8.1，验收固定 tag 安装，并更新 Easydict 的受管副本。
- 允许修改路径：release/changelog/0.8.1.md、本任务 plan/history；Easydict 的六个受管 Skill、skills-lock.json、来源基线及本任务 plan/history。
- 同任务 history：`docs/histories/2026-10/2026-10-23-release-and-upgrade-easydict-v0.8.1.md`
- 用户限制：不创建或切换分支；skills 使用既有 main，Easydict 使用既有 dev。
- 非目标：修改产品代码、项目专属或第三方 Skill、全局安装；推送 Easydict。
- 验收标准：同 SHA CI、annotated tag、Release 全文与固定 tag 安装验证通过；Easydict 快照与 lock 一致且本地提交完成。

## 工作计划

1. 审阅完整 v0.8.0..HEAD 范围，准备 changelog，运行完整验证矩阵。
2. 创建发布提交，push main，等待精确 SHA 的 CI 成功，再创建并推送 annotated tag。
3. 验证 Release workflow、tag 身份与正文、固定 tag 的六个 Skill 隔离安装。
4. 通过规定安装器更新 Easydict，验证快照和目录 hash，完成本地提交。
5. 归档计划，回填并推送发布记录。

## 风险与决策

- 使用补丁版本；运行时脚本无变更，不引入新的依赖或接口。
- 发布 tag 不移动；安装器只更新同来源六个受管 Skill，保留其他来源与项目专属资产。
- 来源仓库首次写入前 HEAD 为 08b21c752391926bce8513af7dae76a939e9bc5d，初始工作树干净。
- Easydict 初始 HEAD 为 8d80bfa219dde99c9c1f2760b59b2df72ad4adef，初始工作树干净。

## 进度

- [x] 完整验证及发布提交。
- [x] 发布及隔离安装验收。
- [x] Easydict 更新、验证及本地提交。
- [x] 记录归档及发布记录 push。

## 验证

- 完整矩阵 137 项通过：git-commit 25、worktree-rebase-merge 6、review-pr 64、review 7、共享契约 5、submit-pr 30。Skill 结构、Python 编译、Shell 语法、空白检查、changelog 和记录文件名均通过。
- 发布提交 `1b40de2c4a1b03dcc117b14a1d089d3445bb2b9c` 已推送 main；同 SHA 的[代码 CI](https://github.com/tisfeng/skills/actions/runs/39813451441)及[文档 CI](https://github.com/tisfeng/skills/actions/runs/39813451546)成功。
- annotated tag v0.8.1：tag object `d033324dd8e3b882ad8694836693df5dfd5e12a6`，peeled commit 与发布 SHA 一致，本地和远程已核验。
- [Release v0.8.1](https://github.com/tisfeng/skills/releases/tag/v0.8.1) 发布于 2026-10-22T16:24:06Z，非 draft、非 prerelease；标题精确为 v0.8.1，正文与 tag 内 changelog 全文一致。
- [Release workflow](https://github.com/tisfeng/skills/actions/runs/39813693889) 成功；skills@1.5.25 从固定远程 tag 隔离安装六个完整技能，56 个文件逐一匹配 archive，目录 hash 和 lock 一致，已安装 CLI 冒烟检查通过。
- Easydict 通过同版本安装器同步六个受管技能，56 个文件和目录 hash 匹配，submit-pr 现有 30 项测试通过；项目专属和第三方 Skill、第三方 lock 条目及符号链接未变。
- Easydict 本地提交 `9aa0a6a90c6f75db4ebb8de507cb502e19491a52`，分支 dev，工作树干净，未 push。
- 本任务仅新增发布文档及同步已验证的文档快照，无生产脚本变更；版本范围与安装增量均已核对，无需独立代码 Review。

## 完成条件

发布与消费者验收完成；Easydict 变更仅本地提交，来源仓库发布记录推送；分支与无关文件保持不变。
