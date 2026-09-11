# 构建、测试与独立核验

## 验证原则

- 先运行与改动直接相关的检查；仅在新变更、失败或未解决风险出现时扩大验证。
- 最终采用的审查和验证必须覆盖最终内容快照；验证后又修改内容时，按风险补充增量复验。
- 同一任务中，相同内容快照、命令和环境的有效验证结果可复用；由一名执行者保留命令、退出
  状态和必要输出，主 Agent 核验其范围与证据。快照或环境变化、失败、证据缺口影响结论时，
  重新运行相关检查，不因换执行者重复验证。
- 相互独立且没有共享写入冲突的检查可并行。
- 尚未解决且经核实的阻塞问题、失败验证或必要证据缺失时不能声称完成或自动提交。
- 纯治理 Markdown、文档重组或低风险配置默认只运行静态检查；用户明确要求构建或测试时，仍按
  请求执行相称的验证。

## 角色边界

子代理的选择、委派条件和权限边界以 [`request-boundary.md`](request-boundary.md) 的
“子代理”一节为唯一来源；本节只补充验证相关的收尾要求。

- Git index 和本地交付始终串行；委派 `tester` 时补充行为预期和验证范围。
- `tester` 返回测试目的、修改路径、实际命令、结果和阻塞证据；主 Agent 核验其范围与证据，
  生产缺陷在已有授权内修复。
- 单独 review 默认只读；上述收尾规则不把 review、planning 或 staged 提交升级为修复任务。

## 本仓库验证

- 每次变更运行 `git diff --check`。
- 修改 Skill、Skill 脚本或 Skill 测试时运行 `python3.12 scripts/validate-skills.py` 和直接相关的
  Python 单测。
- 修改 Skill 依赖、资源引用或跨项目执行行为时，运行
  `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`，验证隔离消费者中的
  安装资产与 helper 行为；它不能替代实际 Agent 对项目规则的理解和执行验证。
- 修改 agent TOML、agent installer、Agent 治理或 agent 目录时运行
  `python3.12 scripts/validate-agents.py`；修改 installer 时运行
  `node --test tests/agents-installer.test.mjs`。
- 修改 Python 时运行针对性单测与 `python3.12 -m compileall -q scripts skills`；修改 Shell 时运行
  `bash -n`；修改 JSON 或 YAML 时使用对应的解析器检查。
- 修改项目技能发现入口或其校验器时运行 `python3.12 scripts/validate-skills.py`，检查公开链接、
  目录链接与内部技能。
- 文档结构变化时检查现行相对链接、锚点和已删除路径引用。仓库校验脚本使用 `tomllib`，应选用
  Python 3.11 或更高版本。

静态检查只能证明仓库文本、脚本和测试快照一致；它不证明 npm 发布、下游安装器发现或 Codex
运行时加载行为。
