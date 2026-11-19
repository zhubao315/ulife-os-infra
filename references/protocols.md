---
title: "protocols"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# 协议层：MCP / A2A / Agent Skills + 冷启动预算（uLife OS v2.1）

三者正交——**MCP 连工具和数据，A2A 连 Agent 与 Agent，Agent Skills 封装可移植能力**。uLife OS 在其上叠加冷启动预算与人机接力闸门。

## 0. 冷启动上下文预算（T1/T2/T3）
- **T1 瞬态**（≤4,000）：`AGENTS.md` + 目标文件；禁全库检索 / 历史日记。
- **T2 领域**（≤16,000）：T1 + 身份契约 + 1–2 个 SKILL.md；禁一次 >3 Skill 全文。
- **T3 编排**（≤32,000 主控）：T2 + L3 语义索引，重活交子 Agent；禁主控吞吐原始工具输出。

## 0.5 人机接力检查点（Human-in-the-Loop Gate）
- **低风险自动放行**：只读 / 内部 / 可逆 / 无外部副作用 → 直接落 `Outbox Receipt`。
- **高风险挂起审批**：对外发送 / 写 USER 域 / 财务·关系·不可逆决策 → `Inbox/Pending` 等 Operator 签字。
- **拒绝/吊销**：触碰硬红线或超授权 → 终止工单记入拒绝回执，不重试绕过。
- 原则：模型可提议，只有人类签字才能跨过外部世界边界。

## 0.6 异构算力与隐私路由
- **本地轻量模型**：高频低延迟、隐私任务（日记信号提取 / FM 补全 / 文档初筛）。
- **云端强推理**：架构设计 / 深度综合 / 复杂重构（仅传脱敏契约与最小切片）。

## MCP（Model Context Protocol）
- AI 应用连接外部系统的开放标准（类比 USB-C）；Claude/ChatGPT/VS Code/Cursor 均支持。
- 2026-07-28 规范：MCP Apps；Dynamic Client Registration 已废弃；默认无状态。
- **安全六项（接 server 前逐项勾选）**：
  1. 无 token passthrough——验 audience（RFC9068）
  2. 元数据发现封私网段 / 强制 HTTPS（仅 loopback 开发例外）
  3. 本地 server 一键配置显式同意 + 沙箱最小权限
  4. state handle 不可预测、服务端绑定已认证用户
  5. scope 从最小起步、按需 step-up 提权（避免 `*` / `all`）
  6. 授权响应校验 iss（PKCE 不能单独防 mix-up）

## A2A（Agent2Agent）
- 不同平台 Agent 间通信的开放标准；与 MCP 互补；v1.0，6 官方 SDK，170+ 伙伴，Apache 2.0，2026-08 加入 Linux Foundation AAIF。
- 关键：互操作、复杂工作流委托、Secure & Opaque（无需共享内部记忆/IP）、可扩展。
- 本 Skill 定位：概念与接入路径已覆盖；SDK 实战列为进阶。
