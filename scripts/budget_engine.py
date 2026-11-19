"""动态上下文预算：Effective Context Budget + 使用率探测。零依赖。"""
import re

DEFAULTS = {"t1": 4000, "t2": 16000, "t3": 32000}
RESERVED_OUTPUT = 0.15   # 预留输出 15%
SAFETY_MARGIN = 0.10     # 安全边际 10%

def effective_budget(window, system_tokens, tool_schema_tokens):
    """Effective = Window - System - Tools - Reserved - Safety."""
    usable = window - system_tokens - tool_schema_tokens
    reserved = int(usable * RESERVED_OUTPUT)
    safety = int(usable * SAFETY_MARGIN)
    return max(0, usable - reserved - safety)

def tier_budget(effective, tier="t2"):
    """按任务级别从有效预算中分配检索额度。"""
    ratio = {"t1": 0.25, "t2": 0.55, "t3": 0.85}.get(tier, 0.55)
    return int(effective * ratio)

def estimate_tokens(text):
    """粗略估算：CJK 约 1 字 1 token，英文约 4 字符 1 token。"""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    other = len(text) - cjk
    return cjk + other // 4

def probe(root):
    """扫描指定目录，返回各文件 token 估算（用于判断挂载成本）。"""
    from pathlib import Path
    out = []
    for p in Path(root).rglob("*.md"):
        out.append((str(p), estimate_tokens(p.read_text(encoding="utf-8", errors="ignore"))))
    return sorted(out, key=lambda x: -x[1])
