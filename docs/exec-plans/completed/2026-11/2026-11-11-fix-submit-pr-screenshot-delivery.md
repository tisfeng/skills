# 修复 submit-pr 截图补传和复验

- 状态：completed
- 创建日期：2026-11-11
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode Unknown (Unknown)`

## 背景

审查发现附件补传可能覆盖上传期间的编辑，复验使用实时 Git 引用，非 UI 变更无法附验证截图。

## 目标与范围

- 目标结果：分开附件上传与正文保存，复验使用冻结回执，支持非 UI 验证截图。
- 允许修改路径：`skills/submit-pr/` 及同任务计划和 history。
- 同任务 history：`docs/histories/2026-11/2026-11-11-fix-submit-pr-screenshot-delivery.md`
- 用户限制：仅本地交付。
- 非目标：修改现有 GitHub PR 或全局安装。
- 验收标准：覆盖并发编辑处理、head/base 漂移与非 UI 截图。

## 工作计划

1. 修改截图渲染、回执复验和附件工作流。
2. 运行现有测试和本地边界验证，审查并归档。

## 风险与决策

- 使用 apply 回执锁定验证对象。附件上传结束后才读回并比较正文，保存与读取之间仍有短暂竞态。

## 进度

- [x] 实现、验证和审查。

## 验证

34 个 submit-pr 测试和 3 个可移植性测试通过。定向模拟覆盖上传期间正文漂移、缓存 base 前进、
head 漂移和非 UI 截图。Skill 校验、Python 编译和差异检查通过。未操作真实 GitHub PR。

## 完成条件

- 审查结论已处理，验证通过并提交计划和 history。
