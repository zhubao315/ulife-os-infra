---
title: "skills"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# 技能系统与确定性优先链

## 决策优先级链
`目标 → 代码 → CLI 工具 → Prompt → Agent 技能`

- 能用确定性代码解决 → 用代码（结果 100% 可预测）
- 把代码封装成 CLI → 方便复用
- 需智能判断 → 才引入 Prompt
- 最高层 → 把 Prompt 封装为可复用 Agent 技能

**为什么**：AI 是概率性的，同一 prompt 可能不同结果；格式转换/计算/文件操作用代码更可靠，只有理解/推理/创意才值得动用概率能力。

## Agent Skills 规范（agentskills.io）
- 目录：`SKILL.md`（必需）+ `scripts/` + `references/` + `assets/`（可选）
- frontmatter：`name`（≤64 字符、小写字母数字连字符、匹配目录名）、`description`（≤1024 字符、含做什么+何时用+触发关键词）
- 选填：`license` / `compatibility` / `metadata` / `allowed-tools`
- **渐进披露**：元数据约 100 token 启动加载 → 正文 <5,000 token 激活加载 → 资源按需；主文件 <500 行，详细材料移到 references。
- 校验：`skills-ref validate ./my-skill`

## Code-as-Glue（脚本编排优先于多轮工具调用）
当任务需连续调用多个外部工具并处理中间数据时，**优先让 Agent 写一段沙箱脚本（Python/TS）在单次执行中串联所有调用**，避免「思考→调工具→读结果→再思考」的往返消耗大量上下文 Token。能 10 行代码解决，绝不花 1,000 Token 祈祷模型稳定。

## 模块化
每个技能遵循 UNIX 哲学——做一件事、做好它；技能之间可组合成复杂工作流。
