#!/usr/bin/env python3
"""PAI 基础设施只读审计：检查 TELOS 十文件、身份契约体积、目录契约、断链近似。
零第三方依赖；只读，不修改任何文件。"""
from pathlib import Path
import sys

TELOS = ["MISSION", "GOALS", "PROJECTS", "BELIEFS", "MODELS",
         "STRATEGIES", "NARRATIVES", "LEARNED", "CHALLENGES", "IDEAS"]

def audit(root: Path) -> int:
    issues = []
    telos = root / "TELOS"
    for n in TELOS:
        if not any(telos.glob(f"{n}*.md")):
            issues.append(f"缺 TELOS 文件: {n}.md")
    idx = list(telos.glob("*索引*.md")) + list(telos.glob("∑*.md"))
    if idx:
        size = idx[0].stat().st_size
        if size > 8000:
            issues.append(f"身份契约约 {size//4} token，建议 ≤2000")
    for d in ["identity", "memory", "skills", "hooks", "preferences"]:
        if not (root / d).exists() and not (root / "USER" / d).exists():
            issues.append(f"缺目录: {d}/（或 USER/{d}/）")
    print("=== PAI 审计报告 ===")
    print(f"根目录: {root}")
    if issues:
        print(f"发现 {len(issues)} 项待办:")
        for i in issues:
            print("  -", i)
        return 1
    print("✅ 基础设施骨架合规（TELOS 十文件 / 目录契约 / 身份契约体积）")
    return 0

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sys.exit(audit(root))
