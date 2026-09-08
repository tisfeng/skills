# 添加 Electron/TypeScript 代码简化规则

- 日期：2026-09-08
- 状态：completed

## 目标

为通用 `code-simplifier` Skill 增加 Electron、TypeScript 和 React 上下文的专项简化规则，
并保持与具体宿主项目解耦。

## 实际变更

- 新增按需加载的 Electron/TypeScript reference，覆盖类型与模块边界、Electron 进程与 IPC、
  React renderer、资源生命周期和验证边界。
- 在 `code-simplifier` 入口增加明确路由，处理其他技术栈时不会加载该 reference。
- 保留 Boss 参考文档中可复用的进程、IPC、类型和 UI 约束，移除 OCU、BOSS、账号、
  简历、窗口焦点与固定 `pnpm` 等项目专属假设。

## 验证

- `python3 scripts/validate-skills.py`：通过，共验证 6 个 Skills。
- 检查 Electron/TypeScript 与 Swift/Xcode reference 路由、文件存在性与项目专属词扫描：通过。
- `git diff --check`：通过。

`skill-creator` 提供的 `quick_validate.py skills/code-simplifier` 因当前 Python 环境缺少
PyYAML 而未能运行；本任务未为文档型 Skill 扩展额外安装依赖。

## 交付

本任务通过自动本地提交门禁交付；不执行 push、pull、rebase、merge 或发布。
