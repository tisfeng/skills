# PR 实现方式审查与需求证据指纹拆分

- 日期：2026-09-12
- 状态：completed
- 关联计划：[PR 实现方式审查与需求证据指纹拆分](../../exec-plans/completed/2026-09-12-review-pr-approach-and-snapshot-granularity.md)

## 目标

`6b851b7` 后，需求证据与 PR 证据共用同一 `pr` fingerprint，任一关联 issue 正文或讨论变化
都会重发整个 `pr` 段；审查要求也只覆盖“实现是否解决目标”，没有要求判断所选实现方式是否足够好。

## 实际变更

- `review_context.py` 拆分归一化职责：`fingerprint_pr` 只覆盖 PR 层证据，`fingerprint_context`
  覆盖需求证据，新增 `source_id`、`source_fingerprint` 与 `content_hash`；`coverage` 改为接收
  `context` section。
- `review_snapshot.py` 把指纹与载荷拆成 `pr`/`context`/`threads`/`checks` 四个 section；
  `refresh` 新增必填 `--expected-context-fingerprint`，需求侧变化只返回 `context`；提供已验证
  前次快照时返回 `context_delta`，只携带新增/变化来源的完整正文、`removed_ids` 与当前全量索引。
- 旧快照缺少 `context` section 或第四组指纹时按既有 `evidence_reset` 全量重读，不新增兼容层。
- `review` 核心与 `review-pr` 都要求评估所选实现方式：当前方案有风险按 P 级 finding 并给出
  替代，无缺陷但存在更优低风险替代放入待确认决策，没有更好方案时明确说明当前方式已足够；
  报告结论由两项改为功能目标、实现方式、代码正确性三项，并在验证区记录方案评估。
- 同步更新 `problem-review.md`、`snapshot-protocol.md`、`report-example.md` 的相关流程与字段。

## 验证

- `python3.12 -B -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：101 项通过。
- `python3.12 -B -m unittest discover -s skills/review/tests -p 'test_*.py'`：10 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：3 项通过（在沙箱外运行，
  因为沙箱内没有 SSH agent socket，测试自身的 `git commit` 会失败）。
- `python3.12 scripts/validate-skills.py`、`python3.12 -m compileall -q scripts skills`、
  `git diff --check` 通过。
- 新增测试覆盖需求变化只返回 `context`、`context_delta` 的新增/变化/移除与覆盖状态、旧快照重置、
  诊断措辞与来源顺序不构成变更，以及可移植性路径上的四组指纹刷新。
- 未执行真实 GitHub PR/API 流程；合成 fixture 不证明真实远端行为或性能收益。

## 交付

仅本地提交，未 push、未发布、未修改全局安装，也未操作真实 PR。
