# 发布 Skills v0.8.1 并更新 Easydict

- 状态：active
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

- [ ] 完整验证及发布提交。
- [ ] 发布及隔离安装验收。
- [ ] Easydict 更新、验证及本地提交。
- [ ] 记录归档及发布记录 push。

## 验证

- 预检：远程最新 Release 为 v0.8.0，v0.8.1 tag/Release 未占用；origin/main 为 055b0c1a7a50b6275f7e21e775f38d8010f66355，是当前 HEAD 的祖先。
- 完整矩阵 137 项通过：git-commit 25、worktree-rebase-merge 6、review-pr 64、review 7、共享契约 5、submit-pr 30；Skill 结构、Python 编译、Shell 语法与空白检查通过。
- 已审阅完整版本差异：公开 Skill 仅修改 submit-pr 的两份语言契约文档，其他差异为历史记录；入口与详细契约一致，无需修改执行脚本。
- changelog 格式和记录文件名校验通过；待发布与安装验收。

## 完成条件

发布与消费者验收完成；Easydict 变更仅本地提交，来源仓库发布记录推送；分支与无关文件保持不变。
