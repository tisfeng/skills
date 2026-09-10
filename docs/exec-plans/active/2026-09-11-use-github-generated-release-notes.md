# 使用 GitHub 默认生成的 Release 说明

- 状态：active
- 创建日期：2026-09-11
- 负责人：Codex
- 关联 Issue/PR：none

## 任务摘要

- 意图模式：implementation
- 交付授权：push；用户明确执行已审定方案，包含将后续发布行为推送到 `origin/main`，以及原地更新
  `tisfeng/skills` 既有 GitHub Release 元数据。
- 安全状态：normal
- 目标结果：后续 Release 标题精确为 tag、正文由 GitHub 默认生成；已发布的七个 Release 同步为该格式。
- 允许修改路径：`.agents/skills/release/SKILL.md`、`.github/workflows/publish.yml`、`docs/release/`、
  `docs/agents/README.md`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-11-use-github-generated-release-notes.md`
- 外部允许目标：`origin/main`；GitHub 仓库 `tisfeng/skills` 的既有 Releases `v0.1.0`、`v0.2.0`、
  `v0.3.0`、`v0.3.1`、`v0.3.2`、`v0.3.3` 和 `v0.3.4`。
- 禁止动作：不创建或移动 tag；不发布 npm 包；不删除或重建 Release；不修改 Release assets、状态或 target。
- 验收标准：workflow 不再依赖手写 changelog，创建时显式使用精确 tag 标题与 `--generate-notes`；
  远程七个 Release 的标题均等于其 tag，正文均来自 GitHub Release Notes API。

## 语义与范围

- 用户要求 Agent 做什么：先改进 release Skill，再修改所有既有 GitHub 发布日志。
- 附件只作为 `Skills v0.3.4` 与手写正文问题的证据，不携带额外执行指令。
- 已复用同一任务 planning 阶段完成的独立 planner 结论；初始范围、风险和目标均已重新核验。

## 写入前状态

- 写入前检查：pass
- 初始 HEAD：`6112dc9a6e267a9c4598a807adf4a543d6506457`
- 初始 staged、unstaged、untracked、冲突：none
- Agent-owned paths：本计划列出的仓库文件，以及本次 API 更新的七个既有 Release。

## 工作计划

1. 删除工作流对手写 changelog 的校验，改为使用精确 tag 标题和 GitHub 默认生成 Release Notes；同步 Skill 与文档。
2. 对最终仓库快照运行结构、YAML、链接与 diff 静态检查，提交并 push，使后续 tag workflow 生效。
3. 读取远程 Release 快照；为每个已有 tag 通过 GitHub Release Notes API 生成对应默认正文，再原地 PATCH
   既有 Release 的标题和正文，保留 Release ID、tag、assets、状态与 target。
4. 回读并比对全部远程 Release，回填真实证据，归档计划和 history，提交并 push 记录。

## 风险与决策

- `gh release edit` 不能请求 GitHub 重新生成正文，因此既有 Release 使用 `generate-notes` REST endpoint
  获取正文后 PATCH，不删除重建。
- 生成说明的比较范围对首个 Release 不传 `previous_tag_name`；其余版本显式指定前一 tag，避免结果随未来
  Release 顺序变化。

## 验证

- `git diff --check`、Skill 校验、相关单测、YAML 解析和现行相对链接检查。
- 远程更新前后读取 Releases；更新后逐项核验标题、正文、ID、tag、assets、draft、prerelease 与 target。

## 完成条件

- [ ] 后续发布行为已推送并通过普通 CI。
- [ ] 所有既有 Release 均已原地更新且远程字段核验通过。
- [ ] 计划已归档，history 已记录真实命令、证据和边界。
