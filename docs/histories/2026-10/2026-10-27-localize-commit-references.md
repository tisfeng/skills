# 按语言区块保留提交引用

- 日期：2026-10-27
- 状态：completed
- 关联计划：[按语言区块保留提交引用](../../exec-plans/completed/2026-10/2026-10-27-localize-commit-references.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B48)`

## 目标

让双语提交的本地语言和英文区块分别包含完整来源，保持单语言格式及其他提交契约。

## 实际变更

- 权威规范改为每个语言区块一个可选 References；双语有引用时两个区块必须同时包含相同顺序的 URL，标签可按语言翻译。单语言继续使用一个可选尾段。
- 校验器先拆分双语区块，再分别提取和校验引用，比较有序 URL 列表；沿用区块内去重、来源 URL 格式、正文和 breaking footer 校验。
- 增加使用腾讯翻译退市通知链接的完整规范示例；仅迁移受旧格式影响的已有测试输入与期望，未新增或扩写测试范围。
- 保留来源准确性、最小来源集合、中性引用、提交预览和 Git 实际消息一致性校验。其他 Git Skill 没有重复定义旧规则，无需修改。

## 验证

- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`：25 个测试通过。
- `python3.12 scripts/validate-skills.py`：6 个 Skill 及发现入口通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：3 个测试通过。
- `git diff --check`：通过。
- 文档完整双语示例与其英文单语言区块通过 CLI 校验；旧的仅英文引用格式、两区块 URL 不一致格式按预期被拒绝。
- 按 review Skill 对初始 HEAD `380da9c0c234ea640a3004ae92908428996e04a9` 后的三项 Skill 文件进行只读审查，核对解析顺序、区块引用一致性、错误路径及现有消息一致性流程，无有效 finding；复用既有解析的实现已足够，无需增加抽象。
- 审查的 SHA-256 快照：规范 `a8610fd77db821a05619bcd87e30c2cd1ca3bc0c82acdc012a969573fd650648`；校验器 `70dbead609675fe64595edd6e2758601eba2a976dfd20eb408f4259a9e97c9e9`；已有测试 `1dfded21c550e41b97fa1a0a0c63010ac2eb45623ff62ed90a29657bb73fe423`。
- 未验证下游 Agent 的实际运行时加载；未改写任何历史提交。

## 交付

- 规范、脚本、已有测试、归档计划和本记录一起按 git-commit 流程本地提交；实际 hash 和最终状态见提交回执。
- 范围仅限 skills 项目；不修改 Easydict，不 push 或执行其他外部写入。
