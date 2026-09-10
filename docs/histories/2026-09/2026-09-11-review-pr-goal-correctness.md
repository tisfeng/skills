# PR 目标与功能正确性审查

## 已落地结果

用户要求先理解 PR 标题、描述和关联 issue 所表达的问题，再判断代码是否真正满足目标。
在保留既有代码审查和提速协议的基础上，完成以下改进：

- 新增只读问题证据采集器，规范化并去重 closing、正文提及、用户指定及讨论来源；
  默认并行读取直接 issue 正文，显式选择的讨论完整分页并复验，不递归遍历背景链接。
- 原始证据与覆盖状态保存在 `pr.reviewContext`，复用原有 PR fingerprint 与快照传输。
  新增 `--issue`/`--issue-comments`，只从验证过的旧快照恢复选择；读取失败保留为缺口。
- 需求正文和采用的讨论变化可在 head 不变时触发刷新；旧快照缺字段不是无需求的证明。
- `review-pr` 前置目标理解，并向 `review` 交付验收条件和来源；在同一次审查中核对实现、
  调用路径和测试。报告分别说明功能满足程度、代码正确性及静态/运行证据。
- 部分修复按明确范围评价，引用不自动升级为要求；保留完整线程/diff、权限和默认不等待 CI。

未修改 Git 准备或远程写入协议，也未修改全局 Skill 安装。

## 验证

- `python3.12 -B -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：89 项通过。
- `python3.12 -B -m unittest discover -s skills/review/tests -p 'test_*.py'`：10 项通过。
- Skill 结构与相对引用校验、两个 Skill 的 quick_validate、Python 编译、`git diff --check` 通过。
- 新增采集和集成测试覆盖身份、去重、正文、讨论分页、失败、需求漂移、旧快照与传输兼容。
- 独立只读代码审查无阻塞 finding；测试中间快照的诊断措辞断言已修正，最终全套通过。
- 独立合成场景演练覆盖主题重启保留、明确 CSV-only 范围、缓存/审计保留冲突和 UTC 格式抽取；
  能识别功能缺口，且不把未运行测试写成实际通过。

上述测试使用本地 fixture，不证明真实 GitHub API 端到端运行、真实 PR 审查效果或固定耗时收益。
没有操作真实 PR、push、发布版本或更新全局配置。

## 关联计划

[PR 功能目标审查](../../exec-plans/completed/2026-09-11-review-pr-goal-correctness.md)
