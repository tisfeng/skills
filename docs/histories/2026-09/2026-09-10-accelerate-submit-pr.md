# 优化 submit-pr 执行延迟

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-accelerate-submit-pr.md)

## 目标

根据一次约 228.5 秒的现有 PR 更新记录，减少 `submit-pr` 正常成功路径中的版本失败重试、重复
Git/GitHub 查询和非必需的 CI 等待，同时保留完整预览、精确 fetch、范围审核、现有 PR 防覆盖、
精确 push、写后身份与 SHA 验证及失败恢复边界。

## 实际变更

- helper 在任何仓库或 GitHub 操作前要求 Python 3.10+；Skill 示例固定使用 Python 3.12，并要求
  同一任务的 `plan` 与 `apply` 复用已选解释器。
- 提交范围从 `rev-list` 加每提交两次 `git show` 改为一次 NUL 分隔的 `git log`，仍保留完整提交
  消息供 `forbid` 策略扫描，多提交、Unicode 和多行正文保持可验证。
- 同一次 `apply` 复用已验证的 push URL；现有 PR 的写前检查直接使用带完整身份字段的
  `gh pr list` 结果，写后仍执行一次 `gh pr view` 和完整验证。
- apply 成功 JSON 新增 `pr_verification` 与 `timings_ms`。调用 Agent 使用该权威回执，不再重复读取
  完整 PR 正文；只有写后验证通过才输出成功结果。
- Skill 明确预览后的正常路径使用程序化工具调用连续等待独立命令，异常、漂移、审批或内容变化
  立即返回模型，不跨 helper 调用缓存远程状态。
- 默认不等待 CI；只有用户或仓库规则明确要求时才单独查询或等待 checks。

## 验证

- `submit-pr` 32 项、`git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项测试通过。
- `python3.12 scripts/validate-skills.py` 验证 6 个 Skill 通过。
- `python3.12 -m compileall -q scripts skills` 与 `git diff --check` 通过。
- 使用本机 Python 3.9 对不存在的仓库路径启动 helper，版本门禁先返回兼容性错误，证明没有进入
  仓库解析；本机 `gh pr list --help` 确认当前版本支持新增的完整验证字段。
- `skill-creator` 的 quick validator 使用系统、项目及工作区 Python 均因缺少 PyYAML 无法启动；
  未安装新依赖，已由仓库自带 Skill 校验器覆盖 frontmatter 和结构检查。
- 独立 reviewer 未发现 finding；补充了其建议的最终 PR 校验失败不输出成功 JSON 的行为测试。

## 交付

本任务按 `auto-local-commit` 精确本地提交；未执行 push、PR 创建或修改、CI 等待、fetch、pull、
rebase、merge、发布或下游安装。
