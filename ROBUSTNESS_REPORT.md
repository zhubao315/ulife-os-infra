---
title: "ROBUSTNESS_REPORT — 10 轮健壮性/易用性测试"
created: 2026-11-19
tags: ["维度/科技", "类型/参考", "来源/项目"]
---

# 健壮性与易用性测试报告（10 轮）

> 基准：2026-11-19 · 每轮发现问题 → 修复 → 回归通过 → 进入下一轮 · 全程 Evidence over Claims。

## 10 轮结果

| 轮 | 场景 | 首次结果 | 发现与修复 |
|---|---|---|---|
| 1 | 单元测试 + CLI 帮助 | PASS | 34 测试 + 15 命令 help 全可用 |
| 2 | 无效/缺参数 | PASS | 无未捕获 traceback |
| 3 | 路径（空格/中文/深层） | PASS | 均正常初始化 |
| 4 | 幂等/冲突/dry-run | PASS | 用户文件不覆盖、未知 profile 拒绝 |
| 5 | **路径安全** | **FAIL→修复→PASS** | 🐛 `safe_join` 未拦截指向自身的 symlink → 改为逐级检查每段 symlink |
| 6 | 审计损坏输入 | PASS* | *首报 FAIL 系测试脚本截断 stdout，修正测试脚本后 PASS（产品无 bug） |
| 7 | 授权边界 | PASS | 过期/错误 Diff/重复消费全拦截 |
| 8 | Memory 边界 | PASS | 非法类型/推断冒充事实被拦截 |
| 9 | Receipt/Routing/Observability | PASS | success 无证据/RESTRICTED 外发/无数据 NOT MEASURED |
| 10 | **文档一致性** | **FAIL→修复→PASS** | 🐛 README 缺 `ulife.py route`、停留在 v1.1 描述 → 全量更新到 v2.0 命令清单与目录结构 |

## 最终回归
10/10 轮 PASS · 34/34 单元测试 PASS · 全库断链 0/锚点 0/FM 100%/标签 0 非标。

## 发现的两个真 bug（均已修复）
1. **轮5 路径安全**：符号链接绕过（安全相关，P0）。
2. **轮10 文档漂移**：README 与 v1.4/v2.0 实现不一致（易用性相关，P1）。

> 测试脚本自身在轮6 有一次误报（stdout 截断），修正测试方法后确认产品无缺陷——记录于此以示诚实。
