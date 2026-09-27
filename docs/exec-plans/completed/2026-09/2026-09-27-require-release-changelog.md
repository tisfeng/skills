# 将版本 changelog 作为 Release 正文来源

- 状态：completed
- 创建日期：2026-09-27
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 背景

现行规则禁止新增版本日志，workflow 自动生成的正文可能只有比较链接。用户要求参照 v0.6.2，
每个版本维护简短中文 changelog，并直接用作 Release 正文。

## 目标与范围

- 目标结果：版本日志成为发布前置条件和正文的唯一来源。
- 允许修改路径：`release/`、`.github/workflows/release.yml`、本任务 plan/history。
- 同任务 history：`docs/histories/2026-09/2026-09-27-require-release-changelog.md`
- 用户限制：本地流程建设，不 push、不发布、不更新线上 Release。
- 非目标：改写旧 tag、历史发布记录或公开 Skill；新增测试代码。
- 验收标准：规则与实现一致；有效日志通过预检；已有 Release 也核验正文；补齐近期日志。

## 工作计划

1. 修改规则、正文规范和 workflow；补录 v0.6.2、v0.6.3、v0.7.0 日志。
2. 运行 YAML、Shell、日志预检、链接及 whitespace 检查。
3. 按 review 技能审查最终实现，修复有效问题，完成记录与本地提交。

## 风险与决策

- 缺失或空白日志阻止发布；API 失败不能当成 Release 不存在。
- 已有正文不一致时失败，不自动覆盖线上内容。
- 新版本日志来自 tag 快照；历史补录不移动公开 tag。
- 正文比对仅统一 CRLF/LF 和末尾换行。

## 进度

- [x] 修改规则、workflow 和近期日志。
- [x] 验证与审查。
- [x] 更新 history、归档计划并提交。

## 验证

- YAML、Shell、内嵌 Python 语法、三份日志预检、相对链接、文件名和 whitespace 检查通过。
- 缺少 v0.7.1 日志时预检退出 1；真实 v0.6.2 正文一致，v0.6.3、v0.7.0 差异被比对表达式识别。
- 最终 review 无有效 finding；直接使用版本文档和标准 CLI 已满足目标。
- 未执行实际发布、线上回填或固定 tag 安装，未新增测试代码。
- 完整证据见同任务 history。

## 完成条件

范围内实现、必要检查与审查通过，history 完整，计划归档并创建本地提交。
