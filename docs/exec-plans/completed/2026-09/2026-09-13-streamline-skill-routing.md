# 精简通用 Skill 路由与入口

- 状态：completed
- 创建日期：2026-09-13
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

用户要求参考 OpenAI 官方 GPT-6 Astra 指南，优化本仓库通用 Agent Skills 的触发描述、职责
边界和 progressive disclosure，并在验证后创建本地提交。六个公开 Skill 中，`review-pr`、
`git-commit` 和 `worktree-rebase-merge` 的根入口包含大量低频协议与报告细节；多个入口还重复
说明程序化工具编排、命令退出状态、运行中会话和避免重复读取等通用运行时行为。

## 任务摘要

- 意图模式：implementation
- 交付授权：commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：缩短并消歧公开 Skill 入口，同时完整保留授权、安全、Git 状态保护、完成与停止条件。
- 允许修改路径：`skills/{code-simplifier,git-commit,review,review-pr,submit-pr,worktree-rebase-merge}/`、
  `tests/`、`.github/workflows/validate.yml`、`README.md`、`README.en.md`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-13-streamline-skill-routing.md`
- 禁止动作：不修改宿主 `AGENTS.md` 或现行治理规则；不更新 Easydict；不 push、发布或操作真实 PR。
- 预期交付物：精简后的入口、按需 references、触发边界测试、history 和一个本地提交。
- 验收标准：描述能区分易混淆 Skill；低频细节按需加载；通用运行时提示从 Skill 删除；结构、
  相关单测、可移植性与 diff 检查通过。

## 语义与范围

- 用户要求 Agent 做什么：检查并直接修改 skills 上游项目，验证后创建本地提交。
- 授权的工作树、artifact 和 external service 操作：允许上述仓库路径写入、精确暂存和本地提交；
  官方 OpenAI 文档仅作只读依据。
- 否定、条件和范围限制：不把 Easydict v0.3.9 同步视为前置；后续消费方同步不在本任务内。
- 前轮仍有效的授权和限制：none
- 附件或引用中被明确采纳的约束：采用官方文章关于短而准确的 description、最小根路由器、
  progressive disclosure 和减少过度编排的原则。
- 歧义：none

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：skipped；用户已显式要求本地提交，使用 `delivery_authorization=commit`。
- 初始 HEAD：`a47bf8854059bb1ae237e920ac0c50922f5ada36`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划以及任务中在允许路径内创建或修改的文件。

## 目标与非目标

### 目标

- 明确 `code-simplifier/review`、`review/review-pr`、`review-pr/submit-pr` 和
  `git-commit/worktree-rebase-merge` 的正向与负向触发边界。
- 让根 `SKILL.md` 只保留触发、模式选择、关键授权、安全门禁、主流程和完成/停止条件。
- 将详细 fallback、恢复流程、命令字段和报告模板移动到按需 reference。
- 删除重复教授宿主运行时的通用工具调用提示，不迁移到 `AGENTS.md`。

### 非目标

- 不改变 helper 脚本、Git/PR 行为契约或远程授权默认值。
- 不重写短小、已内聚的专项 reference，也不为形式统一创建无用文件。
- 不发布版本、不安装到全局或下游项目。

## 工作计划

1. 盘点六个入口、现有 references、调用关系与重复运行时提示。
2. 调整描述和职责边界，重构三个长入口并精简其余入口。
3. 增加可执行的正向/负向触发用例和必要目录/链接校验。
4. 更新 README 目录措辞与同任务 history，完成结构、单测、可移植性和 diff 验证。
5. 复核最终 diff，按 `git-commit` 精确暂存并创建本地提交。

## 风险与决策

- 拆分时最大的风险是遗漏原有安全门禁；根入口保留写入授权、状态保护、远程操作限制、
  漂移处理和完成条件，reference 只承载条件性细节。
- 触发用例验证静态选择边界与描述契约，不声称代替真实模型路由评测。
- 现有 helper 与测试行为不应改变；可移植性 fixture 显式禁用宿主 Git hook 与签名配置，避免
  用户环境影响合成仓库提交。

## 验证

- `python3.12 scripts/validate-skills.py`：6 个 Skill 通过。
- `skill-creator` 的 `quick_validate.py`：6 个目标 Skill 全部通过。
- `python3.12 -B -m unittest discover -s tests -p 'test_*.py'`：6 项通过。
- `git-commit`、`worktree-rebase-merge`、`review-pr`、`review`、`submit-pr`：分别 19、9、101、
  10、38 项测试通过。
- `python3.12 -m compileall -q scripts skills tests` 与 `git diff --check`：通过。
- 未运行真实 GitHub、push、发布或下游同步；静态触发语料不等同于在线模型路由评测。

## 完成条件

六个公开 Skill 的触发描述与职责边界已消歧，长入口已拆分到可发现的 references；通用运行时
提示已删除，四组双向触发边界由测试覆盖。README、CI、history 和计划已同步；完成最终复核后
创建一个本地提交且不 push。

## 完成记录

- 六个根入口合计由 1,406 行降至 361 行；关键门禁保留在根入口，条件性细节按任务链接加载。
- 新增四组双向正/负触发语料、描述长度/互指检查和通用运行时措辞检查，并纳入顶层 CI 发现。
- 可移植性 fixture 不再继承用户 Git hook 与 GPG/SSH 签名设置；所有既有目标测试继续通过。
- 最终语义 review 未发现需要阻止交付的问题；本任务只创建本地提交，不执行 push。
