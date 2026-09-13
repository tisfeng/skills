# 加强 Skill 格式校验

- 状态：completed
- 创建日期：2026-09-13
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

现有 `validate-skills.py` 能检查必填字段存在、目录匹配、文档链接和发现入口，但没有覆盖
Agent Skills 规范对 `name` 与 `description` 的基础长度和格式约束。
用户要求执行精简后的方案，只保留简单、确定性的格式验证，不建立模型路由评测，也暂不验证
独立或组合安装。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：补齐必要 frontmatter 格式校验，并保持当前 OpenAI Skill 工具链兼容。
- 允许修改路径：`scripts/validate-skills.py`、相关 `skills/*/SKILL.md`、一个精简格式测试、
  `tests/README.md`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-13-strengthen-skill-format-validation.md`
- 禁止动作：不增加模型路由评测、外部校验依赖、独立/组合安装验证或 Skill 功能测试；不 push、
  发布或修改全局安装。
- 预期交付物：基础元数据校验、两项表驱动格式测试和任务记录。
- 验收标准：当前 6 个 Skill 通过仓库与官方快速格式校验；代表性非法元数据被拒绝；对应格式测试通过。

## 语义与范围

- 用户要求 Agent 做什么：执行修订后的改进方案。
- 授权的工作树、artifact 和 external service 操作：仅修改本仓库格式校验、Skill frontmatter、
  测试与任务记录；允许自动本地提交。
- 否定、条件和范围限制：移除复杂路由评测；只做简单格式验证；暂不处理独立和组合安装。
- 前轮仍有效的授权和限制：保持测试精简方向，不恢复静态触发语料；不 push。
- 附件或引用中被明确采纳的约束：两条 response annotation 均作为本任务范围约束。
- 歧义：Agent Skills 规范允许可选 `compatibility`，但当前 OpenAI `quick_validate.py` 会拒绝该
  字段；以当前可用工具链兼容性为准，不写入替代元数据。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；初始索引、工作树和 untracked 均为空，允许路径明确。
- 初始 HEAD：`a7dd2b680b19e33e5e50c12851a7c74642ce44f6`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划及本任务在允许路径内新增或修改的文件。

## 目标与非目标

### 目标

- 校验 Skill 名称长度、字符格式、目录一致性和字段重复。
- 校验 description 的单行非空值和规范长度。

### 非目标

- 不测试模型是否选择正确 Skill。
- 不引入 `skills-ref`、PyYAML 或其他依赖。
- 不验证 Skill 的业务功能、独立安装或组合安装。

## 工作计划

1. 提取简单 frontmatter 标量并实现基础规范校验。
2. 用两项表驱动测试覆盖合法值与代表性非法值。
3. 使用当前 OpenAI quick validator 复核全部 Skill；不写入其尚未接受的 compatibility 字段。
4. 运行仓库校验、官方 quick validation、精简测试、Python 编译和 diff 检查。
5. 完成语义 review、history 和计划归档，并按规则创建本地提交。

## 风险与决策

- 仓库统一采用单行 frontmatter 标量，使校验保持简单；不尝试实现通用 YAML 解析器。
- 不添加当前 OpenAI quick validator 尚未接受的 `compatibility`、实验性 `allowed-tools` 或无用途
  的 UI 元数据。
- 格式测试只验证确定性结构，不对 description 文案或触发效果作结论。

## 验证

- `python3.12 scripts/validate-skills.py` 通过，验证 6 个 Skill 及项目发现入口。
- 新增的 2 项 frontmatter 格式测试通过。
- 当前 OpenAI `skill-creator` 的 `quick_validate.py` 对 6 个 Skill 逐项验证通过。
- `python3.12 -m compileall -q scripts tests` 与 `git diff --check` 通过。
- 未运行模型路由、Skill 功能、独立安装或组合安装评测，符合用户明确限定的验证范围。

## 完成条件

格式校验修改通过全部约定检查；没有新增功能评测或安装流程；history 与 completed plan
齐全；本地提交完成且未 push。
