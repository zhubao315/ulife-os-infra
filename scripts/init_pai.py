#!/usr/bin/env python3
"""初始化 PAI 骨架（只创建缺失文件，不覆盖、不删除）。零第三方依赖。"""
from pathlib import Path
import sys

TELOS = ["MISSION", "GOALS", "PROJECTS", "BELIEFS", "MODELS",
         "STRATEGIES", "NARRATIVES", "LEARNED", "CHALLENGES", "IDEAS"]
TPL = "---\ntitle: {n}\n---\n\n# {n}\n\n> 引导问题见 SKILL.md 的 references/telos.md\n\n1. \n2. \n3. \n"

def main(root: Path):
    made = []
    for d in ["TELOS", "USER/identity", "USER/preferences", "USER/workflows",
              "USER/skills", "USER/hooks", "USER/memory", "SYSTEM"]:
        p = root / d
        if not p.exists():
            p.mkdir(parents=True)
            made.append(f"目录 {d}/")
    for n in TELOS:
        p = root / "TELOS" / f"{n}.md"
        if not p.exists():
            p.write_text(TPL.format(n=n), encoding="utf-8")
            made.append(f"TELOS/{n}.md")
    print(f"初始化完成，新建 {len(made)} 项（未覆盖任何已有文件）")
    for m in made:
        print("  +", m)

if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./my-pai"))
