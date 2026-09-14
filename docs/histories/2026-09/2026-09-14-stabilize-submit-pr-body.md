# 固定 submit-pr 正文结构

- 日期：2026-09-14
- 状态：completed
- 关联计划：[固定 submit-pr 正文结构](../../exec-plans/completed/2026-09/2026-09-14-stabilize-submit-pr-body.md)

## 目标

使 `submit-pr` 无论目标仓库是否包含 GitHub PR 模板，都只使用 Skill 自带的固定正文结构；将原
Summary 拆分为 Context 与 Changes，并保留现有 Issue、验证、截图和远程写入安全边界。

## 实际变更

- 新增独立的 `assets/pull_request_template.md`，固定 Context、Changes、Linked Issues、
  Verification 和 Screenshots 五段；helper 从自身安装位置加载并校验必需占位符。
- 删除目标仓库模板发现、标题别名、段落合并、`--template`、`--extra-body-file`、`--summary`
  和 plan 的模板路径字段，新增必填 `--context` 与 `--changes`。
- 更新调用 Agent 契约，明确不读取目标仓库 PR 模板；仓库明确规则与固定结构冲突时停止，不恢复
  模板合并。
- 新增真实故障回归，覆盖仓库模板中的 `变更摘要`、`验证情况`、`关联上下文`、多模板并存、
  旧 CLI 快速失败及旧版 PR 正文防覆盖。
- 隔离消费者验证复制后的 Skill 会携带并使用自带模板，消费者仓库模板不会进入生成正文。

## 验证

- `python3.12 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'`：18 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 scripts/validate-skills.py`：6 个 Skill 与仓库发现入口通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `skill-creator` 的 `quick_validate.py skills/submit-pr`：通过。
- `git diff --check`：通过。
- 未运行真实 GitHub PR 创建或复用流程；集成测试使用临时 Git 仓库和模拟 GitHub。

## 交付

仅创建本地提交；未 push、未发布版本、未修改全局 Skill 安装，也未操作真实 PR。
