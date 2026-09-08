# 加固 PR 提交与 Agent 安装流程

- 状态：completed
- 创建日期：2026-09-08
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

只读审查发现 `submit-pr` 不能在已有 PR 上快进推送新提交，且使用 remote 名称推送时只验证
了一个 push URL；Agent installer 则会在批量冲突时留下部分写入，并静默忽略本地来源的 ref。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：修复四项已确认的问题，并保留空暂存区时允许一次 `git add .` 的现有约定。
- 允许修改路径：`skills/submit-pr/`、`src/cli.mjs`、`tests/agents-installer.test.mjs`、
  本计划与对应 history。
- 同任务 history：`docs/histories/2026-09/2026-09-08-harden-pr-and-agent-installer.md`
- 禁止动作：不修改 Agent 校验器；不发布、不 push、不改用户全局配置。
- 预期交付物：实现、回归测试、Skill 契约文档、完成计划、history 和本地提交。
- 验收标准：已有 PR 可安全快进更新；多 push URL 写入前失败；批量安装冲突零部分写入；
  本地 ref 不再被静默忽略；相关测试与仓库校验通过。

## 语义与范围

- 用户要求 Agent 做什么：按已确认方案修复问题。
- 授权的工作树、artifact 和 external service 操作：修改当前仓库并自动本地提交。
- 否定、条件和范围限制：保留初始空暂存时运行一次 `git add .`；暂不修改 Agent 校验器。
- 前轮仍有效的授权和限制：不自动发布或 push。
- 附件或引用中被明确采纳的约束：六条审查注释中的四项修复确认与两项范围更正。
- 歧义：none。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；implementation、初始索引为空且路径可隔离。
- 初始 HEAD：`ce7d090517c10ffde18d4c147878df9d6a9f70ea`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：允许修改路径中本任务实际产生差异的文件。

## 目标与非目标

### 目标

- 在复用 PR 前校验不可变字段，安全推送后再校验完整远程状态。
- 将 push 操作绑定到唯一、已验证的 URL。
- 将 Agent 批量安装改为预检后提交，避免可预见冲突造成部分写入。
- 明确定义并验证本地来源 ref 的行为。

### 非目标

- 不改变 `git-commit` 的空索引自动暂存约定。
- 不新增 Agent 角色契约校验。
- 不执行真实 GitHub 或 npm 写入。

## 工作计划

1. [x] 补充失败场景测试并修复 `submit-pr` 的已有 PR 与 push URL 流程。
2. [x] 补充多 Agent 和本地 ref 测试，重构 installer 的预检与原子提交。
3. [x] 同步 Skill 契约、完成 history，并运行针对性与全量验证。
4. [x] 通过 Git 门禁后精确暂存并自动本地提交。

## 风险与决策

- 保留维护者修改保护：已有 PR 的标题、正文、Draft、仓库和分支必须在 push 前一致。
- 仅允许远程 head 是计划 HEAD 祖先时更新，分叉继续 fail closed。
- 本地 ref 采用显式拒绝方案，避免为 installer 引入改变来源 checkout 的复杂状态操作。

## 验证

- `python3 scripts/validate-skills.py`：通过，6 个 Skills。
- `python3 -m compileall -q skills scripts`：通过。
- `python3 scripts/validate-agents.py`：通过，4 个 Agents。
- `node --test tests/agents-installer.test.mjs`：通过，6 项。
- `python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`：通过，19 项。
- `python3 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：通过，27 项。
- `python3 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'`：通过，23 项。
- `bash -n skills/review-pr/scripts/prepare-pr-branch.sh`、`node --check src/cli.mjs`：通过。
- `npm pack --dry-run`：通过，使用 `/private/tmp` cache 绕过用户 npm cache 权限问题。
- `git diff --check`：通过。
- Skill Creator 的 `quick_validate.py` 因当前 Python 缺少 PyYAML 未运行成功；仓库自带 Skill
  validator 已通过。未安装新依赖以避免修改用户环境。
- 本地没有 Node 20 runtime，installer 在 Node 24.19.0 验证；CI 仍会覆盖声明的 Node 20 下限。
- 未执行真实 GitHub push 或 PR 写入；相关行为由本地 bare remotes 和 fake `gh` 集成测试覆盖。

## 完成条件

- [x] 所有验收标准有自动化测试覆盖。
- [x] 最终 diff 通过仓库校验。
- [x] 计划与 history 已完成，进入自动本地提交。
