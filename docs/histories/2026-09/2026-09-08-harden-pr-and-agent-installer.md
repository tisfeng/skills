# 加固 PR 提交与 Agent 安装流程

- 日期：2026-09-08
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-08-harden-pr-and-agent-installer.md`](../../exec-plans/completed/2026-09-08-harden-pr-and-agent-installer.md)

## 目标

修复 `submit-pr` 的已有 PR 更新和 push URL 边界，以及 Agent installer 的批量一致性与本地
ref 语义，同时保留用户指定的 `git-commit` 空索引自动暂存行为。

## 实际变更

- `submit-pr` 在复用已有 PR 前校验维护者控制字段，允许远程 head 从祖先提交普通快进，并在
  push 后复验完整 PR 状态；本地任务分支仅允许同步快进。
- 所有 head push 都使用唯一、已验证的 GitHub push URL；多 push URL 配置在远程写入前停止。
- Agent installer 改为全量冲突预检后写入；运行期写入失败时恢复已写目标和原 lock。
- 本地来源携带 `#ref` 时给出明确错误，Git URL 仍支持版本 ref；CLI 帮助同步说明该边界。
- 保留 `git-commit` 在初始暂存为空且存在变动时允许一次 `git add .` 的用户指定行为；未修改
  Agent 校验器。

## 验证

- Skills 与 Agent validator、Python compileall、Node 语法、Shell 语法和 `git diff --check`
  通过。
- 75 项自动化测试通过：Agent installer 6、git-commit 19、review-pr 27、submit-pr 23。
- `npm pack --dry-run` 通过；Skill Creator 的独立 quick validator 因当前 Python 缺少 PyYAML
  未能运行，仓库自带 Skill validator 已通过。
- installer 在本地 Node 24.19.0 验证；Node 20 下限留给现有 CI 覆盖。
- 没有真实 GitHub 写入；PR 行为通过本地 bare remotes 与 fake `gh` 验证。

## 交付

- 本任务通过自动本地提交门禁交付；未 push、发布或修改用户全局 Codex 配置。
