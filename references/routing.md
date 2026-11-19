---
title: "动态上下文预算与模型路由"
created: 2026-11-19
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# 动态上下文预算与模型路由（v1.3）

## Effective Context Budget（评审点 09）
```
Effective = Model Window - System Instructions - Tool Schemas - Reserved Output - Safety Margin
```
- Reserved Output ≈ 有效值 15%，Safety Margin ≈ 10%（可配置）。
- T1/T2/T3 是**起步默认值**（4k/16k/32k），不是固定上限。
- `ulife.py budget --window 200000 --system 4000 --tools 8000 --tier t2` 实算。

## Model Routing Policy（评审点 10）
| 任务 | 默认路由 | 关键因素 |
|---|---|---|
| 日记情景识别 | 本地 | 隐私、成本 |
| Frontmatter 补全 | 本地 | 规则性 |
| 普通文件检索 | 本地 | 数据位置 |
| 复杂架构研究 | 云端 | 推理能力 |
| 跨领域综合 | 云端或混合 | 复杂度 |
| 私密内容分析 | 本地优先 | 数据敏感度 |
| 高风险决策 | 人类主导 | 不可委托性 |

## 数据分级
`PUBLIC / INTERNAL / PRIVATE / RESTRICTED`。未经授权，PRIVATE/RESTRICTED 不得自动发往云端模型。
