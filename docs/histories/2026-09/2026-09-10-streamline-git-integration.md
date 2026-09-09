# 精简已有提交的 Git 集成流程

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-streamline-git-integration.md)

## 目标

参考「查找废弃文档」任务中的性能调查和最终方案，减少已有提交集成的代理往返，保留完整
输出、新提交预览、用户确认限制和现有模型配置。

## 实际变更

- worktree-rebase-merge 为干净的已有提交增加一次委派内检查和集成路径。
- 新增只读 snapshot/verify 脚本，收集源/目标 HEAD、分支身份、索引摘要、worktree 状态与占用、
  提交清单、历史路径并集、merge-base 和 Git 元数据路径；复验发现漂移时返回阻塞。
- git-delivery 和宿主 Git 规则对齐连续集成阶段、精简上下文、已知受限位置提权及完整回执复用。
- 新提交仍遵循原有 prepare/apply 预览与暂存契约；不改变 git-commit、模型、推理强度或 sandbox。

## 验证

- 独立 planner 评估；tester 新增 9 项真实临时 Git 仓库测试。
- worktree 单测共 11 项、git-commit 单测 19 项通过。
- 覆盖只读性、正常 rebase/merge、源/目标脏状态、HEAD/分支身份/占用漂移、名称冲突、
  临时目标、撤销/重命名/换行路径、冲突中状态、读取权限错误和远程默认分支解析。
- 读取权限错误采用局部模拟，不代表实际沙箱审批拒绝验证。
- validate-skills、validate-agents、Skill quick_validate、compileall、git diff --check 通过。
- reviewer 发现脚本门禁误覆盖新提交流程，修复后增量复核无剩余阻塞项。
- 5 次正常 snapshot 脚本用时 0.75、0.66、0.61、0.60、0.61 秒；未进行同模型 5 次端到端
  集成基准，不声称达到 2 分钟目标或验证运行时重新加载。

## 交付

- 初始 HEAD 为 `07c73fc5e8d2a8a8b72a32e6060663a130b0fd62`，初始工作树与索引干净。
- 实施期间外部 pull 快进至 `31fedaa117008f575987100e9f0475c986906d5f`，本任务新增文件保留，
  已按新基础适配并验证。因初始 HEAD 漂移，自动提交门禁暂停；未自动暂存或提交。
- 用户随后明确调用 git-commit，以当前 HEAD 重新冻结范围，按显式提交工作流完成本地交付。
- 本轮仅更新上游源码，未 push、发布、同步 Easydict 或修改全局安装资产。
