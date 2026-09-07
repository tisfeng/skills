# 完整提交回执示例

仅在需要组织最终用户可见回复时阅读。替换所有示例事实；`SKILL.md` 的
Post-Commit Report 规则和 Git 的实际输出优先。

````markdown
本地 Git 提交完成。

提交结果

- 动作：已创建提交
- Commit：`0123456789abcdef0123456789abcdef01234567`
- 分支：`docs/unify-git-delivery-receipts`

变动统计

| 类别 | 文件数 | 新增行 | 删除行 | 净变动 |
| --- | ---: | ---: | ---: | ---: |
| 总计 | 5 | 68 | 15 | +53 |
| 代码 | 1 | 8 | 2 | +6 |
| 文档 | 4 | 60 | 13 | +47 |

实际提交信息

```text
docs(git): 统一本地 Git 交付回执

现有提交流程收集了完整结果，但最终回执格式分散，可能被压缩成提交标题。

统一用户可见回执并使用 Markdown 表格展示统计，保留提交信息校验和 JSON 统计数据来源。

这让本地提交提供一致、可核验的结果，并继续保持默认不推送的边界。

----------------------------------------------------------------------

docs(git): unify local Git delivery receipts

The existing commit workflow collected complete results, but its final receipt could be reduced to a commit subject.

Unify the user-visible receipt and render statistics as a Markdown table while preserving message validation and the JSON statistics source.

This gives local commits consistent, verifiable results while preserving the default no-push boundary.
```
````
