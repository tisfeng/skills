# 固定 submit-pr 正文结构

- 状态：completed
- 创建日期：2026-09-14
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`submit-pr` 原先会发现、读取并合并目标仓库的 GitHub PR 模板。仓库模板使用未识别的语义标题时，
helper 会先保留这些段落，再追加内置段落，造成正文结构重复且输出不稳定。

## 目标与范围

- 目标结果：只使用 Skill 自带的 `pull_request_template.md`，将正文固定为 Context、Changes、
  Linked Issues、Verification 和 Screenshots 五段。
- 允许修改路径：`skills/submit-pr/`、`tests/test_skill_portability.py`、本计划及对应 history。
- 同任务 history：`docs/histories/2026-09/2026-09-14-stabilize-submit-pr-body.md`
- 用户限制：本轮实施并创建本地提交；不 push、不发布版本。
- 非目标：不修改 Git/GitHub 拓扑、push、PR 复用或最终验证行为。
- 验收标准：目标仓库模板不再影响输出；新 CLI、固定正文、旧 PR 防覆盖和隔离消费者行为通过验证。

## 工作计划

1. 新增 Skill 自带的独立正文模板并让 helper 确定性渲染。
2. 删除仓库模板发现、语义别名、正文合并及过时 CLI/数据字段。
3. 更新 Skill 入口、工作流契约和调用参数。
4. 更新行为测试和隔离消费者测试，覆盖真实重复正文故障。
5. 运行完整相关验证，记录 history，审查并创建本地提交。

## 风险与决策

- `--summary`、`--template` 和 `--extra-body-file` 不再兼容；旧调用应快速失败并迁移到
  `--context` 与 `--changes`。
- 已有旧正文 PR 会因正文不匹配而停止，不自动覆盖维护者内容。
- 独立模板作为唯一正文结构来源；helper 不复制标题，也不读取目标仓库模板。

## 进度

- [x] 新增并接入固定正文模板。
- [x] 删除旧模板兼容链并更新契约。
- [x] 更新并通过行为验证。
- [x] 完成最终审查、history 和本地提交准备。

## 验证

- `submit-pr` 18 项行为测试与 2 项隔离消费者测试通过。
- 6 个公开 Skill 通过仓库校验，`submit-pr` 通过 `skill-creator` quick validate。
- Python 编译与 `git diff --check` 通过。

## 完成条件

- 固定正文行为及回归场景已通过，最终 diff 无无关变更，计划已归档并进入本地提交交付。
