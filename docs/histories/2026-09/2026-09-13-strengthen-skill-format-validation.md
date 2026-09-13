# 加强 Skill 格式校验

- 日期：2026-09-13
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-13-strengthen-skill-format-validation.md)

## 目标

以少量确定性检查补齐 Skill frontmatter 的基础格式约束，不增加模型路由评测、功能评测或安装
场景，并保持当前 OpenAI Skill 工具链可用。

## 实际变更

- `validate-skills.py` 新增单行必填标量解析，校验重复字段、空值和 block scalar。
- `name` 现在校验 64 字符上限、小写字母/数字/单连字符格式及目录一致性；`description` 校验
  非空和 1,024 字符上限。
- 新增 2 项表驱动格式测试，覆盖合法 frontmatter 与代表性的缺失、重复、非法、过长输入。
- 在测试保留标准中明确公开 Skill frontmatter 与发现入口属于应保留的确定性格式约束。
- 曾按方案尝试添加 `compatibility`，但当前 OpenAI `skill-creator` 的快速校验器会拒绝该字段；
  最终未修改任何 Skill frontmatter，也未用私有 metadata 绕过工具链限制。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，验证 6 个 Skill 及项目发现入口。
- `python3.12 -m unittest discover -s tests -p 'test_validate_skills.py'`：2 项通过。
- 对 6 个 Skill 逐项运行 OpenAI `skill-creator/scripts/quick_validate.py`：全部通过。
- `python3.12 -m compileall -q scripts tests`：通过。
- `git diff --check`：通过。
- 未运行模型路由、Skill 功能、独立安装或组合安装评测。

## 交付

本任务按 `auto-local-commit` 精确本地提交；未执行 push、fetch、pull、rebase、merge、发布、
模型评测或安装操作。
