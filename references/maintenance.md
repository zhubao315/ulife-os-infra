---
title: "maintenance"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# 可持续改进闭环（Revalidate 引擎 · uLife OS v2.1）

设施不是一次性文档，而是"用 → 测 → 改 → 验 → 回写"的活系统。

## 五步回路
1. **用**：按意图表选一条，真实任务跑一遍（不空转）。
2. **测**：跑 `bash quality_gate.sh` + 记录摩擦点与**返工率（Rework Rate）**——哪步上下文溢出？哪份规范未被检索？
3. **改**：只改现有文件，不新建系统；小步、可回滚。
4. **验**：断链 0 / 锚点 0 / FM 合规 / 标签 0 非标，四项全绿。
5. **回写**：有效改动写回对应章节 + 升级版本；无效尝试标注作废而非删除留痕。

## 成熟度自检（10 项，每月勾一次）
1. TELOS 十文件存在且每季更新
2. 身份契约 ≤2,000 token 且按需挂载
3. 日记 / 回执连续不断档
4. 静默审计脚本全绿
5. uSkill 能力包化（SKILL.md 合规比例）
6. MCP 安全六项全勾
7. A2A 协议接入（进阶）
8. 文档可发现性（意图表覆盖高频场景）
9. 链接健康（断链 0 / 锚点 0）
10. 闭环至少跑过 1 轮

## 质量门：Standalone / Integrated 双模式（v1.2）

> **Standalone Mode（无需外部脚本）**：本 Skill 自带工具，任何用户安装即可用。
```bash
python3 scripts/ulife.py audit --target <your-pai> --format json   # 五层审计
python3 -m unittest discover -s tests                              # 回归测试
```

> **Integrated Mode（可选，对接你已有的基础设施）**：路径必须参数化，不得硬编码。
```bash
ULIFE_TOOLS_DIR="${ULIFE_TOOLS_DIR:-<your-tools-dir>}" bash "$ULIFE_TOOLS_DIR/quality_gate.sh"
python3 "$ULIFE_TOOLS_DIR/link_checker.py" --full
python3 "$ULIFE_TOOLS_DIR/anchor_lint.py"
python3 "$ULIFE_TOOLS_DIR/frontmatter_check.py"
python3 "$ULIFE_TOOLS_DIR/tag_audit.py"
```
> 个人知识库的绝对路径（如原 `/data/obsidian/hermes/09-REFERENCE/93-脚本`）不得出现在公开文档中；用 `ULIFE_TOOLS_DIR` 环境变量替代。

放行标准：**PASS ≥ 阈值、ERROR = 0、NOT CHECKED 显式列出**。没有数据依据的项不得标绿。

> **收官期护栏**：若处于交付冲刺期，任何基础设施优化先答「它服务哪项具体交付？」答不出一律冻结——杜绝用打磨工具替代实际交付。

## 维护节律
- 每次改动后：跑质量验证
- 每周：看意图表是否需加新场景
- 每月：跑自检清单，变化写入版本行
- 每季：重审 TELOS + 指南是否匹配业界进展
