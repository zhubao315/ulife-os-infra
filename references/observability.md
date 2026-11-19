---
title: "v2.0 Observability — 10 指标健康报告"
created: 2026-11-19
tags: ["维度/科技", "类型/参考", "来源/项目"]
---

# Observability（v2.0）

## 10 指标（口径 + 数据源）
任务成功率 / 返工率 / 上下文效率 / 记忆准确率 / Skill 复用率 / 策略违规率 / 审批率 / Agent 失败率 / 恢复成功率 / 维护成本。

- 可从 Outbox / memory_engine 自动计算：任务成功率、Agent 失败率、记忆准确率。
- 需 Runtime 埋点或用户记录：**返工率、上下文效率、Skill 复用率、维护成本**——无数据时一律 `NOT MEASURED`。

## 铁律
**不得用没有数据依据的指标显示绿色健康状态。** `ulife.py observe` 输出即健康报告。

## 委托与验证
`orchestration_engine`：统一 Task Contract + 最小信息委托 + expected_output 结果验证。
