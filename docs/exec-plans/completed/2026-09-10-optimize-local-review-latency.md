# 优化本地 review 执行效率

## 目标与授权

用户已授权实施本地 `review` 性能方案：批量预检、冻结证据复用、按需检索、只读 commit/range
快照 helper 和行为测试。保留完整审查范围、raw patch、验证与最终复验；不改变 Skill 路由、
模型或推理强度，也不混入 `review-pr` 修复。外部推送、发布和用户全局安装不在范围内。

## 初始快照与范围

- initial_head：`a421d5db1b20b98fbc05dee010166e131f65431d`。
- 当前分支：`main`；初始 staged、unstaged、untracked 均为空，无冲突。
- task_allowed_paths：`skills/review/SKILL.md`、`skills/review/scripts/`、`skills/review/tests/`、
  `.github/workflows/validate.yml`、本计划及同任务 history。
- agent_owned_paths：本次在以上范围新增或修改的文件；交付前冻结精确清单。
- 遵循用户此前不希望直接提交 main 的要求，本轮不自动在 main 创建提交；保留可审查修改。

## 工作计划

1. 为普通 commit/range 增加批量收集及紧凑复验；范围不明确时返回可操作错误。
2. 增加有限大小、显式分页的 raw patch，记录完整哈希与覆盖偏移；其他审查模式沿用原流程。
3. 补充 Skill 的证据复用、针对性检索和验证收敛规则，保留现有契约。
4. 用临时仓库测试 parent/range、root、脏工作树保护、内容完整性和漂移，接入既有 CI。
5. 校验结构、编译、差异和链接；用 `83c25a4` 回放 helper，记录实际输出与耗时。
6. 独立只读审查最终实现，处理有效问题，完成计划与 history。

## 风险与验收

- 不把工作树源码或测试误记为历史提交证据；commit/range 读取冻结 Git 对象。
- `A..B` 与 `A...B` 区分，merge commit 不默认选 parent；浅克隆证据缺失必须报错。
- 禁用外部 diff/textconv 和自动 fetch；helper 不写索引、ref 或对象，不启动远程流程。
- 大 patch、特殊路径、二进制、删除、文件 mode 等不能静默遗漏；分页完成由连续覆盖证明。
- 输出精简不等于语义审查已完成；测试与端到端性能分别报告，不承诺 90–150 秒目标已达成。
- 本任务为 review 单模块改进，主 Agent 负责方案；按仓库规则委派 tester 和最终 reviewer。

## 进度

- 已完成全部实施步骤；helper、Skill 协议、9 项行为测试及 CI 入口已落地。
- 9 项测试通过，运行 6.075 秒；同时验证索引、HEAD/refs、各类文件字节调用前后未改变。
- 结构、编译、Skill quick validation、YAML 与差异检查通过；独立 reviewer 未发现明确缺陷。
- `83c25a4` 的两页 patch 拼接与 Git diff 字节一致；5 次首页 CLI 调用 138.73–151.64 ms，
  未变化复验输出 569 字节。只报告 helper 测量，不推断完整 Agent 端到端耗时。
- 完成记录：[`同任务 history`](../../histories/2026-09/2026-09-10-optimize-local-review-latency.md)。
- 实现阶段保留工作区修改；用户随后显式调用 `git-commit`，交付续办使用
  `codex/perf-local-review-latency` 任务分支，不直接提交 main，也不执行远程交付。
