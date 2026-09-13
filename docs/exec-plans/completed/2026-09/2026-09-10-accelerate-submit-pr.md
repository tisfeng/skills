# 优化 submit-pr 执行延迟

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

一次现有 PR 更新的窄口径耗时约 228.5 秒，其中独立命令墙钟时间约 41.3 秒。主要等待来自
Python 运行时失败重试、预览后的多轮 Agent/工具编排、重复 PR 全量读取和非必需的 CI 等待。
用户要求保留现有安全与功能边界并实施性能优化，同时明确默认不等待 CI。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 目标结果：减少 submit-pr 正常成功路径的命令与模型往返，并提供可定位的 helper 分阶段计时。
- 允许修改路径：`skills/submit-pr/`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-10-accelerate-submit-pr.md`
- 禁止动作：不 push、不创建或修改 PR、不等待 CI、不省略精确 fetch、漂移检测、冲突保护或最终验证。

## 写入前状态

- 初始 HEAD：`ab956382fcb8de8fe5254cd62d88b6f31b130b21`
- 初始分支：`perf/accelerate-git-skill-execution`
- 初始 staged、unstaged、untracked、冲突：none
- Agent-owned paths：本计划及上述允许路径内本任务实际新增或修改的文件。

## 工作计划

1. 固定并前置验证 Python 3.10+ 运行时，避免完成远程发现后才失败。
2. 批量读取提交元数据，减少提交范围检查的子进程数量。
3. 让 apply 的最终校验结果携带完整而紧凑的权威回执和分阶段计时，取消调用方重复读取。
4. 明确默认不等待 CI；预览后以程序化工具调用连续等待独立命令，只在异常或漂移时返回模型。
5. 补充真实行为测试，运行针对性测试、Skill 校验、Python 编译、diff 检查与独立只读审查。
6. 归档计划、写入 history，并按 auto-local-commit 精确本地提交。

## 验证结果

- `submit-pr` 32 项、`git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项测试通过。
- Skill 仓库校验、Python compileall 和 `git diff --check` 通过。
- Python 3.9 实际启动在仓库解析前被版本门禁拒绝；当前 GitHub CLI 支持新增 PR list 字段。
- 独立 reviewer 未发现 finding；最终验证失败不输出成功回执的增量测试已补充。
- `skill-creator` quick validator 因所有可用 Python 环境缺少 PyYAML 未启动，使用仓库校验器替代。

## 风险与完成条件

- 不跨 plan/apply 缓存远程状态；apply 仍重新发现并精确 fetch。
- 现有 PR 的 title、body、Draft、仓库身份和 SHA 不匹配时继续失败关闭，不自动覆盖。
- helper 的成功 JSON 只能来自实际 push 后最终 PR 验证。
- 默认不运行 CI watch；用户或仓库明确要求时才单独执行。
- 最终快照通过相关测试和独立审查，无未解决 finding。
