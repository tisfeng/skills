# 统一 submit-pr 的用户语言选择

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex
- 关联 Issue/PR：[#1](https://github.com/tisfeng/skills/pull/1)

## 背景

当前 `submit-pr` 要求调用 Agent 起草标题与正文，但没有规定用户首选语言的解析顺序。实际 PR #1
因此接收了 Agent 起草的英文标题、Summary 和 Verification，尽管当前对话使用中文。helper 只原样
渲染参数，这一确定性边界应继续保留。

## 任务摘要

- 意图模式：implementation
- 交付授权：push
- 安全状态：normal
- 受阻操作及原因（如有）：无
- 目标结果：为 PR 起草新增明确的用户语言契约，验证 Unicode 内容保真，并修正 PR #1 的标题和正文。
- 允许修改路径：`skills/submit-pr/SKILL.md`、`skills/submit-pr/references/workflow.md`、
  `skills/submit-pr/tests/test_submit_pr.py`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-10-prefer-submit-pr-language.md`
- 禁止动作：不改变 helper 的权限、拓扑、push、恢复或已有 PR 防覆盖边界；不 merge 或发布。
- 预期交付物：经过验证的 Skill 契约、行为测试、本地提交、更新后的分支和 PR #1 metadata。
- 验收标准：中文对话默认生成中文 PR 内容；模板和技术标识保留；测试与仓库校验通过；PR 读回一致。

## 语义与范围

- 用户要求 Agent 做什么：执行上一轮已确认的改进方案。
- 授权的工作树、artifact 和 external service 操作：修改仓库文件、本地提交、推送当前任务分支、
  更新 PR #1 的 title/body 并读回核验。
- 否定、条件和范围限制：保持现有功能与安全边界，不把自然语言推断放入 deterministic helper。
- 前轮仍有效的授权和限制：当前工作必须保留 PR #1，不直接提交到 `main`。
- 附件或引用中被明确采纳的约束：采用 `git-commit` 的用户语言来源思想，但 PR 对话语言优先于
  系统 locale，且 PR 默认不复制双语提交信息结构。
- 歧义：无；本轮“执行”承接已明确说明的本地与远程步骤。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：skipped；用户已授权包含 push 和 PR metadata 写入的显式交付流程。
- 初始 HEAD：`8547338f5a47d865ff7ed920c57f818ecfd5dfb6`
- 初始 staged 路径：无
- 初始 unstaged 路径：无
- 初始 untracked 路径：无
- 初始冲突：无
- Agent-owned paths：允许修改路径中的本任务新增或修改文件。

## 目标与非目标

### 目标

- 让调用 Agent 在起草 PR 前解析并展示用户首选语言及来源。
- 让标题 subject、Summary、Verification 和 Agent 自拟说明默认使用所选语言。
- 用 helper 的真实 plan/apply fixture 验证中文参数从输入到 GitHub 状态保持不变。
- 保留模板内容、固定双语结构和已有 PR 不一致时停止的行为。

### 非目标

- 不让 Python helper 猜测、翻译或校验自然语言。
- 不增加通用的已有 PR 自动改写模式。
- 不修改 `git-commit`、PR 提交历史、分支结构或发布配置。

## 工作计划

1. 更新 `submit-pr` 入口与工作流契约，建立单一语言决策来源和模板边界。
2. 增加中文标题与正文的 plan/apply 保真测试，并保留英文兼容覆盖。
3. 运行针对性测试、Skill 校验、Python 编译和 diff 检查，进行独立只读复核。
4. 更新 history、归档本计划，使用 `git-commit` 精确提交并通过 `submit-pr` 更新远程分支。
5. 写前复验 PR #1 后只更新 title/body，最后读回核对不变量。

## 风险与决策

- 对话语言优先于系统 locale，避免英文终端 locale 覆盖明确的中文会话；用户显式要求始终最高。
- 目标仓库明确的 PR 语言要求是硬约束；英文模板或提交历史本身不构成该要求。
- helper 保持语言无关和原样传递，防止弱语言检测造成误判，也保持现有调用兼容性。
- PR #1 metadata 通过一次窄范围 `gh pr edit` 修正；若写前内容漂移则停止，不覆盖维护者变化。

## 验证

- `submit-pr` 29 项测试通过，其中中文 plan/apply 保真及已有英文 PR 防覆盖为新增覆盖。
- `git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项和 Agent installer 6 项通过，
  合计 90 项自动化测试。
- 6 个 Skill 与 3 个 Codex agent 结构校验、Python 编译、Shell 语法和 `git diff --check` 通过。
- `skill-creator` 的独立 quick validator 已尝试，但两个可用 Python runtime 均缺少 `PyYAML`，
  因环境依赖未启动；本仓库 `scripts/validate-skills.py` 已成功验证全部 Skill。
- 独立只读 reviewer 无 finding；真实 GitHub push 与 PR metadata 读回在本地提交后执行。

## 完成条件

- 契约和测试覆盖最终快照，独立 review 无阻塞 finding；本地提交、push 与 PR #1 读回由交付步骤
  完成并在最终回执记录。
