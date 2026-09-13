# 构建与测试

## 验证原则

- 先运行与改动直接相关的检查；仅在新变更、失败或未解决风险出现时扩大验证。
- 最终审查和验证覆盖最终内容快照。相同快照、命令和环境的有效结果可复用；内容、
  环境或证据变化并影响结论时，重新运行相关检查。
- 尚未解决且经核实的阻塞问题、失败验证或必要证据缺失时不能声称完成或自动提交。
- 纯治理 Markdown、文档重组或低风险配置默认只运行静态检查；用户明确要求构建或测试时，仍按
  请求执行相称的验证。

## 本仓库验证

- 每次变更运行 `git diff --check`。
- 修改 Skill、Skill 脚本或 Skill 测试时运行 `python3.12 scripts/validate-skills.py` 和直接相关的
  Python 单测。
- 修改 Skill 依赖、资源引用或跨项目执行行为时，运行
  `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`，验证隔离消费者中的
  安装资产与 helper 行为；它不能替代实际 Agent 对项目规则的理解和执行验证。
- 修改 Python 时运行针对性单测与 `python3.12 -m compileall -q scripts skills`；修改 Shell 时运行
  `bash -n`；修改 JSON 或 YAML 时使用对应的解析器检查。
- 修改项目技能发现入口或其校验器时运行 `python3.12 scripts/validate-skills.py`，检查公开链接、
  目录链接与内部技能。
- 文档结构变化时检查现行相对链接、锚点和已删除路径引用。

静态检查只能证明仓库文本、脚本和测试快照一致；它不证明 Skill 安装、下游发现或运行时加载
行为。
