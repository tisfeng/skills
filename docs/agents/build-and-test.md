# 构建、测试与独立核验

## 验证原则

- 先运行与改动直接相关的检查；仅在新变更、失败或未解决风险出现时扩大验证。
- 最终采用的审查和验证必须覆盖最终内容快照；验证后又修改内容时，按风险补充增量复验。
- 尚未解决且经核实的阻塞问题、失败验证或必要证据缺失时不能声称完成或自动提交。
- 纯治理 Markdown、文档重组或低风险配置默认只运行静态检查；用户明确要求构建或测试时，仍按
  请求执行相称的验证。

## 角色边界

- 有行为风险的 implementation 优先使用只读 `reviewer`；需要编写测试或复杂独立验证时使用
  `tester`。简单文档、低风险配置或小改动由主 Agent 完成必要检查。
- Git index 和本地交付始终串行。委派 tester 时补充行为预期和验证范围；tester 只修改明确分配的
  测试与 fixture，不修改生产代码、工程配置或 history，也不执行 stage、commit、push 或 Git ref
  操作。
- tester 返回测试目的、修改路径、实际命令、结果和阻塞证据；生产缺陷交回主 Agent。主 Agent 核验
  审查意见，在已有授权内修复真实问题。
- 单独 review 默认只读；上述收尾规则不把 review、planning 或 staged 提交升级为修复任务。

## 本仓库验证

- 每次变更运行 `git diff --check`。
- 修改 Skill、Skill 脚本或 Skill 测试时运行 `python3.12 scripts/validate-skills.py` 和直接相关的
  Python 单测。
- 修改 agent TOML、agent installer、Agent 治理或 agent 目录时运行
  `python3.12 scripts/validate-agents.py`；修改 installer 时运行
  `node --test tests/agents-installer.test.mjs`。
- 修改 Python 时运行针对性单测与 `python3.12 -m compileall -q scripts skills`；修改 Shell 时运行
  `bash -n`；修改 JSON 或 YAML 时使用对应的解析器检查。
- 文档结构变化时检查现行相对链接、锚点和已删除路径引用。仓库校验脚本使用 `tomllib`，应选用
  Python 3.11 或更高版本。

静态检查只能证明仓库文本、脚本和测试快照一致；它不证明 npm 发布、下游安装器发现或 Codex
运行时加载行为。
