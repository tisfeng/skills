# 精简通用 Skill 路由与入口

- 日期：2026-09-13
- 状态：completed
- 关联计划：[精简通用 Skill 路由与入口](../../exec-plans/completed/2026-09-13-streamline-skill-routing.md)

## 目标

依据 OpenAI 关于短而准确的 Skill 描述、最小根路由器和 progressive disclosure 的建议，消除
六个通用 Skill 的重叠触发与重复运行时提示；在不削弱授权、安全、Git 状态保护和停止条件的
前提下，把低频协议移到按需 references，并创建本地提交。

## 实际变更

- 缩短 `code-simplifier`、`review`、`review-pr`、`submit-pr`、`git-commit` 和
  `worktree-rebase-merge` 的触发描述，并在每组易混淆 Skill 中明确正向职责与替代入口。
- 将提交信息/分支命名/回执、commit/range 快照、PR 本地准备/证据/报告，以及 worktree
  集成/恢复/回执拆为按需 references；六个根 `SKILL.md` 合计由 1,406 行降至 361 行。
- 根入口继续保留写入授权、只读边界、精确暂存、脏工作树保护、禁止隐式 push/远程写入、
  漂移处理和完成/停止条件；删除通用工具调用、退出码、运行中会话和重复读取提示。
- 新增四组成对的双向正/负触发语料与静态测试，同时检查 description 长度、替代 Skill 互指和
  被移除的通用运行时措辞；CI 改为发现顶层全部 `test_*.py`。
- 同步 README 中公开 Skill 目录说明。可移植性测试的合成 Git 仓库显式禁用宿主 hook 与
  GPG/SSH 签名配置，避免用户环境污染 fixture，不改变产品 Skill 行为。

## 验证

- `python3.12 scripts/validate-skills.py`：6 个 Skill 通过。
- `skill-creator` 的 `quick_validate.py`：6 个目标 Skill 全部通过。
- `python3.12 -B -m unittest discover -s tests -p 'test_*.py'`：6 项通过。
- `git-commit`、`worktree-rebase-merge`、`review-pr`、`review`、`submit-pr`：分别 19、9、101、
  10、38 项测试通过。
- `python3.12 -m compileall -q scripts skills tests` 与 `git diff --check`：通过。
- 最终语义 review 未发现 actionable finding。未运行真实 GitHub/API 流程；静态触发语料不证明
  在线模型的实际选择率。

## 交付

仅创建本地提交；未 push、未发布、未修改全局安装、未同步 Easydict，也未操作真实 PR。
