---
title: "v1.4 安全治理 — 数据分级与风险矩阵"
created: 2026-11-19
tags: ["维度/科技", "类型/参考", "来源/项目"]
---

# 安全治理（v1.4）

## 数据分级
`PUBLIC < INTERNAL < PRIVATE < RESTRICTED`。
PRIVATE / RESTRICTED 未经显式授权不得发往云端模型；`policy_engine.can_send_external()` 强制拦截。

## 风险矩阵
| 操作 | 级别 | 需授权 | 可外发 |
|---|---|---|---|
| 只读 | L0 | 否 | 是 |
| 内部可逆写 | L1 | 否 | 是 |
| USER 资产写 | L2 | 是 | 否 |
| 外部发送 | L3 | 是 | 是 |
| 不可逆 | L3 | 是 | 否 |

## 边界
`ULIFE_GUARD_ACK=1` 仅为意图标识；真实权限由操作系统 / Agent Host / 独立权限代理执行。
用户本人始终拥有管理与删除个人数据的权利（Agent 默认不得物理删除）。
