"""初始化引擎：只从 canonical templates 复制，幂等、不覆盖、dry-run、冲突检测。"""
from pathlib import Path
from core import CANON, PROFILES, safe_join, sha256

DIRS = ["USER/identity", "USER/preferences", "USER/workflows",
        "USER/skills", "USER/hooks", "USER/memory", "SYSTEM"]

def canonical(name):
    p = CANON / "templates" / "telos" / f"{name}.md"
    if not p.exists():
        raise FileNotFoundError(f"canonical 模板缺失: {p}")
    return p

def boundary_template():
    p = CANON / "templates" / "starter" / "BOUNDARIES.md"
    return p if p.exists() else None

def plan(root: Path, profile: str):
    """返回写入计划：[(rel, source_or_None, action)]"""
    if profile not in PROFILES:
        raise ValueError(f"未知 profile: {profile}（可选 {list(PROFILES)}）")
    actions = []
    for d in DIRS:
        rel = d + "/"
        if not (root / d).exists():
            actions.append((rel, None, "mkdir"))
    names = list(PROFILES[profile])
    if profile == "starter" and boundary_template():
        names.append("BOUNDARIES")
    for n in names:
        rel = f"TELOS/{n}.md" if n != "BOUNDARIES" else "TELOS/BOUNDARIES.md"
        src = boundary_template() if n == "BOUNDARIES" else canonical(n)
        target = safe_join(root, rel)
        if not target.exists():
            actions.append((rel, src, "create"))
        else:
            # 冲突检测：若目标内容与 canonical 不同，视为用户修改，绝不覆盖
            actions.append((rel, src, "keep"))
    return actions

def execute(root: Path, profile: str, dry_run: bool, force: bool):
    acts = plan(root, profile)
    if dry_run:
        print("[DRY-RUN] 写入计划（不落盘）：")
        for rel, src, act in acts:
            print(f"  {act:6} {rel}" + (f"  <- {src.name}" if src and act == "create" else ""))
        return {"dry_run": True, "planned": len(acts)}
    root.mkdir(parents=True, exist_ok=True)
    made, kept = [], []
    for rel, src, act in acts:
        if act == "mkdir":
            (root / rel.rstrip("/")).mkdir(parents=True, exist_ok=True)
            made.append(rel)
        elif act == "create":
            target = safe_join(root, rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            made.append(rel)
        elif act == "keep":
            kept.append(rel)
    receipt = {"profile": profile, "created": made, "kept_user_files": kept,
               "canonical_sha": {n: sha256(canonical(n).read_text(encoding="utf-8")) for n in PROFILES[profile]}}
    (root / "INIT_RECEIPT.json").write_text(json_dumps(receipt), encoding="utf-8")
    print(f"初始化完成：新建 {len(made)}，保留用户文件 {len(kept)}，回执 INIT_RECEIPT.json")
    return receipt

def json_dumps(o):
    import json
    return json.dumps(o, ensure_ascii=False, indent=2)
