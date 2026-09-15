# 移植 Scoco Agent 治理规则

<!-- 文件名：YYYY-MM-DD-<slug>.md；命名规则见 docs/agents/README.md 的“Plan 与 History”。 -->
<!-- 本模板只用于多步骤、跨模块或高风险的执行任务。 -->

- 状态：completed
- 创建日期：2026-09-15
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

本仓库的 Agent 文档落后于 Scoco `dev` 的现行治理规则，缺少测试代码的明确授权门禁，编码规范
仍使用旧文件名，Plan 与 History 的命名约定也未同步稳定标识规则。此次按本仓库边界进行语义
移植，不复制 Scoco 的 Swift、Xcode、应用资产或外部 Skill 管理规则。

## 目标与范围

- 目标结果：对齐可复用的测试授权、编码规范和文档命名规则。
- 允许修改路径：`AGENTS.md`、`docs/agents/`、`docs/exec-plans/templates.md`、
  `docs/histories/template.md`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-15-port-scoco-agent-governance.md`
- 用户限制：参考最新 Scoco `dev`，按 skills 仓库实际技术和资产边界移植。
- 非目标：不修改 Skill 源码、测试、发布流程、外部服务或历史记录正文。
- 验收标准：现行路由无旧文件引用；规则语义和链接检查通过；创建 Angular-style 本地提交。

## 工作计划

1. 重命名并补强编码规范，更新根任务路由。
2. 增加测试代码明确授权门禁，同时保留本仓库现有验证矩阵。
3. 同步 Plan 与 History 的月份和稳定标识规则及模板引用。
4. 创建 history，运行静态检查，归档计划并本地提交。

## 风险与决策

- 使用语义移植，避免引入 Scoco 专属的 Swift、Xcode、本地化和受管资产规则。
- 历史 plan/history 中的旧路径属于历史事实，不进行批量改写。

## 进度

- [x] 完成现行规则修改。
- [x] 完成静态验证与历史记录。
- [x] 归档计划并创建本地提交。

## 验证

- `git diff --check` 通过。
- 现行路由、相对链接、锚点和已删除路径引用检查通过。
- 测试授权规则和项目专属验证规则同时保留。

## 完成条件

- 所有计划内文档完成修改并通过静态检查。
- 本计划已归档到 `completed/2026-09/`，同任务 history 链接本计划。
- 本任务差异以一个本地提交交付，且未执行 push。
