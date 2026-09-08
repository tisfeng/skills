# 构建与测试

- 为行为或正确性风险新增有价值的测试；纯文档、明显透传或已有充分覆盖的改动不机械补测试。
- 先运行与改动直接相关的检查；仅在新变更、失败或未解决风险出现时扩大验证。
- 交付前采用的审查和验证必须覆盖最终内容快照；验证后又修改实现时，按风险补充增量复验。
- 有效阻塞 finding、必要验证失败或证据缺失时不能声称完成，也不能自动提交。
- 每次变更运行 `git diff --check`。
- 修改 Python 时运行针对性单测与 `python3 -m compileall -q`；修改 Shell 时运行 `bash -n`；修改
  TOML 时运行 `python3 scripts/validate-agents.py`；修改 Skills 时运行
  `python3 scripts/validate-skills.py`。
- `tester` 只在明确获得测试/fixture 路径写入授权时修改文件；它不暂存、不提交，也不修复生产代码。
- 对同一共享资源避免并发写入或并发执行互相干扰的测试。
