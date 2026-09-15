# 简化提交语言选择并本地化正文标记

- 状态：completed
- 创建日期：2026-09-15
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`git-commit` 的语言优先级先读取平台 locale、最后才使用当前对话语言，规则还枚举了多个
平台变量，难以快速理解。提交正文虽然固定为背景、变更和影响三段，但没有可扫描的段落标记；
用户已选择中文区块使用 `背景：`、`变更：`、`影响：`，英文区块使用小写英文标记。

## 目标与范围

- 目标结果：先使用明确语言偏好和当前对话语言，仅在无法判断时回退系统偏好语言；为三个正文段
  增加顺序固定的本地化标记。
- 允许修改路径：`skills/git-commit/references/commit-message.md`、
  `skills/git-commit/references/post-commit-report-example.md`、
  `skills/git-commit/scripts/validate-commit-message.py`、
  `skills/git-commit/tests/test_validate_commit_message.py`、`tests/test_skill_portability.py`、
  本计划和同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-15-localize-commit-body-labels.md`
- 用户限制：中文使用 `背景：`、`变更：`、`影响：`；英文使用 `context:`、`change:`、`impact:`；
  保留双语、`BREAKING CHANGE`、`References` 和不 push 边界。
- 非目标：不修改标题、分隔线、引用尾段、提交统计或回执字段，不为其他非英文语言新增翻译映射。
- 验收标准：新提交必须按顺序使用完整标记；缺失、错序、混用或空内容会失败；breaking footer 和
  references 尾段继续工作。

## 工作计划

1. 简化并重排语言选择规则，定义中文、英文及其他本地语言区块的正文标记。
2. 重构语言区块校验，保留 footer 行为并严格检查三个标记及非空内容。
3. 按用户批准的方案更新现有测试及回执示例，覆盖正反向组合。
4. 运行针对性、Skill、portability、Python 和 diff 验证。
5. 使用 `review` 审查最终快照，修复有效 finding，归档计划并创建本地提交。

## 风险与决策

- 这是新提交信息格式的强制变化；旧 Git 历史不改写，汇报已有提交仍读取真实消息。
- 中文使用全角冒号且不加空格；英文小写标记使用半角冒号和一个空格。
- 其他非英文语言暂用小写英文标记，避免引入不完整且无法校验的多语言映射。
- 校验器只检查结构，不尝试从正文内容推断自然语言；实际标签选择仍由提交信息契约约束。
- 用户已通过确认此前包含测试更新的方案并要求执行，因此允许更新现有测试用例和 helper。

## 进度

- [x] 核对当前语言、正文、breaking footer、references 和回执示例契约。
- [x] 更新契约、实现、测试和示例。
- [x] 完成验证与审查。
- [x] 写入 history 并归档计划；本地提交由后续精确交付完成。

## 验证

- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`：19 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 scripts/validate-skills.py`：6 个公开 Skills 和仓库发现入口通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `git diff --check`：通过。
- `review`：对基线 `f586c1dd4d45ae7c574db2cd1f6910672824261b` 后的任务变更完成只读审查，
  无 finding；标记选择、顺序、空内容以及 breaking/reference 组合均有对应验证。
- `skill-creator` 的 `quick_validate.py` 未运行成功：当前 Python 环境缺少其 `PyYAML` 依赖；
  未为此临时安装依赖，仓库自身的 Skill 校验已通过。
- 未运行真实 Agent 或安装态 Skill 测试；portability 测试验证了隔离消费者中的复制资产。

## 完成条件

- 新格式和保留的 footer/reference 组合通过测试，旧无标记格式按设计被拒绝。
- Skill、隔离消费者、Python 和 diff 校验通过。
- 最终审查没有阻塞 finding，计划已归档且 history 记录真实结果。
