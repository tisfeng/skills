# PR 实现方式审查与需求证据指纹拆分

- 状态：completed
- 创建日期：2026-09-12
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`6b851b7` 为 `review-pr` 增加了 PR 目标与功能正确性核对，但需求证据与 PR 证据共用同一个
`pr` fingerprint，任一关联 issue 正文或讨论变化都会重新回传整个 `pr` 段；同时审查要求
只覆盖“实现是否解决目标”，没有要求判断所选实现方式是否足够好。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：无
- 目标结果：需求证据独立成 `context` section 与 fingerprint；`review-pr` 与 `review` 要求
  并报告实现方式评估。
- 允许修改路径：`skills/review-pr/`、`skills/review/`、本计划与同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-12-review-pr-approach-and-snapshot-granularity.md`
- 禁止动作：push、发布、真实 PR 操作、修改全局安装、修改无关文件。
- 预期交付物：脚本、测试、Skill 与 references 文本、plan、history。
- 验收标准：相关单测与可移植性测试通过；`validate-skills.py` 通过；需求变化只回传需求证据。

## 语义与范围

- 用户要求 Agent 做什么：修改 `review-pr`/`review` 的审查要求，并修复需求证据的指纹粒度。
- 授权的工作树、artifact 和 external service 操作：仅本地文件与本地 Git；不访问 GitHub。
- 否定、条件和范围限制：无 push、无发布、不扩大为其他改进（如 coverage 三态）。
- 前轮仍有效的授权和限制：只做本地交付，保留既有权限与“不等待 CI”行为。
- 附件或引用中被明确采纳的约束：需求变化不应重发无关 PR 证据；实现方式评估写入结论第三项。
- 歧义：无。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible（索引为空，工作树干净）
- 初始 HEAD：`955a826e8d50bc62add079ddaee1c1b1776081d8`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：上述允许修改路径

## 目标与非目标

### 目标

- 指纹与载荷拆成 `pr`/`context`/`threads`/`checks`；需求变化只回传 `context`。
- `refresh` 支持 `--expected-context-fingerprint` 与 `context_delta`。
- `review` 核心与 `review-pr` 都要求评估实现方式，并在报告结论中给出判断。

### 非目标

- 不调整 `coverage` 三态、checks/threads 指纹、Git 准备与线程协议。
- 不为旧快照写兼容层；旧快照走既有 `evidence_reset` 全量重读。
- 不把“验收条件抽取结果”持久化为机器权威。

## 工作计划

1. 拆分 `review_context` 的归一化与指纹函数，新增来源标识与内容指纹。
2. 调整 `review_snapshot` 的采集、复验、刷新与 CLI，新增 `context` section 与 `context_delta`。
3. 更新 `review-pr` 与 `review` 的审查要求、报告格式与 references。
4. 更新并补充测试：需求变化只回传 `context`、上下文增量、旧快照重置、可移植性。
5. 运行验证、写 history、归档计划并本地提交。

## 风险与决策

- `context_delta` 依赖“传输层措辞不是证据”的归一化；用测试固定诊断措辞与来源顺序不构成变更。
- CLI 由三组指纹变为四组，属于同一 Skill 内的同步变更；旧快照只多付一次全量重读。
- 键位从 `pr.reviewContext` 变为顶层 `context`，收尾用全仓搜索核对文档引用。

## 验证

- `python3.12 -B -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`
- `python3.12 -B -m unittest discover -s skills/review/tests -p 'test_*.py'`
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`
- `python3.12 scripts/validate-skills.py`、`python3.12 -m compileall -q scripts skills`、`git diff --check`
- 记录实际检查、结果、未运行项及证明边界。

## 完成条件

正常与失败路径测试通过，文档引用一致，history 与计划归档完成，本地提交不 push。

## 完成记录

- 指纹与载荷已按 `pr`/`context`/`threads`/`checks` 四组拆分，需求侧变化只返回 `context`，
  有已验证前次快照时返回 `context_delta`；旧快照走既有 `evidence_reset` 全量重读。
- `review` 核心与 `review-pr` 均要求实现方式评估，报告结论与验证区已加入对应字段。
- `review-pr` 101 项、`review` 10 项单测与 3 项可移植性测试通过；Skill 校验、编译与
  `git diff --check` 通过。
- 未执行真实 GitHub 流程；沙箱内缺少 SSH agent socket，可移植性测试在沙箱外运行。
