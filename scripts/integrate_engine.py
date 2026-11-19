"""Integrate 模式：发现现有资产 → 识别现状 → 生成适配方案（不自动建平行系统）。"""
from pathlib import Path

DISCOVER = {
    "claude_md": ["CLAUDE.md", "AGENTS.md"],
    "skills": ["**/SKILL.md"],
    "mcp": ["*mcp*.json", "*mcp*.yaml", "**/mcp_server.py"],
    "memory": ["**/MEMORY.md", "**/memory/*.md"],
}

def discover(root):
    root = Path(root)
    found = {}
    # Obsidian：检测 .obsidian 目录与 md 数量（不是把所有 md 当资产列表）
    md_count = len(list(root.glob("**/*.md")))
    found["obsidian"] = ([".obsidian/"] if (root / ".obsidian").is_dir() else []) + [f"{md_count} 篇 md"]
    for kind, pats in DISCOVER.items():
        hits = [str(p.relative_to(root)) for pat in pats for p in root.glob(pat) if p.is_file()]
        found[kind] = sorted(set(hits))[:20]
    return found

def propose(root):
    d = discover(root)
    lines = ["# Integrate 适配方案（需用户审批后执行）", "",
             "## 发现到的现有资产", ""]
    for k, v in d.items():
        lines.append(f"- **{k}**: {len(v)} 项" + ("（" + ", ".join(v[:5]) + "…）" if v else "（未发现）"))
    lines += ["", "## 建议", ""]
    if d["obsidian"] or d["claude_md"]:
        lines.append("- 已有知识库/上下文文件：走 Audit → 挂载适配，禁止新建平行 TELOS。")
    if d["skills"]:
        lines.append("- 已有 Skills：登记到清单，做规范对齐而非重写。")
    if d["mcp"]:
        lines.append("- 已有 MCP Server：先过六项安全准入，再纳入 Registry。")
    if not any(d.values()):
        lines.append("- 未发现现有资产：可走 Initialize 模式从零搭建。")
    lines += ["", "> 本方案只输出建议，不自动改动任何现有文件；禁止未经审计直接新建平行系统。用户审批后方可 Evolve。"]
    return "\n".join(lines)
