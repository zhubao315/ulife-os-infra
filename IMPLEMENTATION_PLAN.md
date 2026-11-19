---
title: "IMPLEMENTATION_PLAN — v1.2 → v2.0"
created: 2026-11-19
tags: ["维度/科技", "类型/框架", "来源/项目"]
---

# 迭代计划

| 版本 | 目标 | 核心交付 | 状态 |
|---|---|---|---|
| **v1.2** | 工程修复 | 统一 CLI + canonical 初始化 + 五层审计 + 一次性授权 + tests/CI + frontmatter 规范 | **本次执行** |
| v1.3 | 易用性 | Starter/Audit First/Integrate/Migration + 动态预算 | 下一步 |
| v1.4 | 专业能力 | Memory Schema 完整实现 + Policy 数据分级 + Receipt + Routing | 规划 |
| v2.0 | 系统化治理 | Observability + Agent Orchestration + Evolution Engine | 规划 |

## v1.2 验收（本次必须全绿）

1. `python3 scripts/ulife.py init --target <tmp> --profile starter` 生成 5 文件且来自 canonical 模板。
2. 重复 init 不覆盖用户修改；`--dry-run` 只打印计划。
3. `audit --format json` 输出五层结果，含 NOT CHECKED 语义。
4. 一次性授权凭据可生成/校验/过期/撤销。
5. `python3 -m unittest discover -s tests` 全通过；CI 工作流存在。
6. `skills-ref validate .` 通过（如环境可用）。
