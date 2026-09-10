# 优化本地 review 执行效率

## 已实现行为

- `review` 按冻结快照、语义审查与针对性验证、最终复验组织执行，合并无依赖读取，复用有效
  上下文中的规则、patch 和测试证据。保留原审查范围、报告与权限契约。
- 新增 `collect_review_snapshot.py`，支持普通/root/显式 parent 提交和两种 range；从 Git 对象
  读取准确端点与 raw patch，输出 NUL 安全的变更清单、内容 fingerprint 和采集时间。
- 默认每页 24000 字符，记录完整 patch 哈希、总长度及连续偏移；不会将最后一页误标为全部
  覆盖。普通 Unicode 保持可读，无效 UTF-8 字节使用可逆 JSON 转义。
- 复验通过 fingerprint 省略未变化路径清单与 patch，发生变化则返回新证据。checkout 状态单独
  报告，不把当前源码和测试归属给不同的历史提交。helper 不写 Git 状态、不自动 fetch。
- 外部依赖检索围绕具体证据缺口展开，后续查询要求明确线索；保留必要官方核实，不设置固定
  次数或优先级门槛。相关测试接入既有 GitHub Actions 验证工作流。

## 验证与测量

- 临时仓库 9 项行为测试通过（6.075 秒），覆盖 root/merge parent、两种 range、多 merge-base、
  非法输入、脏工作树隔离、含 tab/换行的路径与 symlink/mode、二进制/无效 UTF-8 分页、浅克隆
  缺失 parent 和引用移动复验；确认调用前后索引、HEAD/refs、各类状态及文件字节完全不变。
- 仓库 Skill 校验、Python 编译、Skill quick validation、工作流 YAML 解析和 diff 格式检查通过。
  quick validation 所需 PyYAML 装在任务临时目录，未新增项目或用户全局 Python 依赖。
- 独立 reviewer 审查脚本、Skill 和 CI 接入，未发现明确缺陷；实际单提交采集和未变化复验通过。
- 用 `83c25a46910bbd8488ead1b46362f3e0805659f0` 回放：6 个变更文件，完整 patch 为 40670
  字节；默认两页拼接结果与相同选项的 Git diff 逐字节一致。
- 5 次首次采集 CLI 调用（含 Python 启动、内部完整 diff 计算及首页输出）耗时
  138.73–151.64 ms，中位数 142.19 ms；最终未变化复验 143.05 ms。
- 两页 JSON 输出合计 46817 字节，未变化复验输出 569 字节。以上只测 helper，不能证明完整
  Agent 审查已达到 90–150 秒目标，也未通过修改模型、推理强度或重启对话改变测量条件。

## 交付边界

- 初始 HEAD：`a421d5db1b20b98fbc05dee010166e131f65431d`，初始工作树干净。
- 改动仅包含 review Skill、只读脚本、相关测试、CI 测试入口和本任务文档。
- 实现阶段按用户要求保留工作区修改。用户随后显式调用 `git-commit`，交付续办使用
  `codex/perf-local-review-latency` 任务分支；不直接提交 main，不 push、发布或修改全局安装。
- 同任务执行计划：[`本地 review 优化`](../../exec-plans/completed/2026-09-10-optimize-local-review-latency.md)。
