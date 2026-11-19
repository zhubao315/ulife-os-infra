"""五层审计：Structure / Content / Security / Operational / Value。
不能检查的项标 NOT CHECKED，不默认通过。输出 JSON + Markdown。"""
from pathlib import Path
from core import Report, TELOS, PROFILES, safe_join, parse_fm, strip_fm

def run(root: Path, profile="standard") -> Report:
    r = Report()
    required = list(PROFILES.get(profile, TELOS))
    if profile == "starter":
        required.append("BOUNDARIES")  # Starter 含边界契约

    # L1 Structure：仅本档必需文件缺失才判 ERROR；非本档文件标 NOT CHECKED
    for n in TELOS:
        p = root / "TELOS" / f"{n}.md"
        if n in required:
            r.add("L1", f"TELOS/{n}.md", "PASS" if p.exists() else "ERROR",
                  "存在" if p.exists() else "缺失")
        else:
            r.add("L1", f"TELOS/{n}.md", "PASS" if p.exists() else "NOT CHECKED",
                  "存在" if p.exists() else f"非 {profile} 档必需，不判定失败")
    for d in ["USER/identity", "USER/memory", "USER/skills", "SYSTEM"]:
        r.add("L1", f"目录 {d}/", "PASS" if (root/d).exists() else "WARNING",
              "存在" if (root/d).exists() else "缺失（starter 档可后补）")
    idx = list((root/"TELOS").glob("*索引*.md")) + list((root/"TELOS").glob("∑*.md"))
    if not idx:
        r.add("L1", "身份契约索引", "NOT CHECKED", "未找到索引文件，无法估算体积")
    else:
        size = idx[0].stat().st_size
        est = size // 4
        r.add("L1", "身份契约体积", "PASS" if est <= 2000 else "WARNING",
              f"约 {est} token（可配置阈值 2000）")

    # L2 Content
    for n in TELOS:
        p = root / "TELOS" / f"{n}.md"
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        fm = parse_fm(t)
        r.add("L2", f"{n} Frontmatter", "PASS" if "title" in fm else "WARNING",
              f"title={fm.get('title','缺失')}")
        body = strip_fm(t).strip()
        r.add("L2", f"{n} 正文非空", "PASS" if len(body) > 30 else "WARNING",
              f"{len(body)} 字符")
    # 内部双链检查（基础版：[[目标]] 目标文件是否存在于 root 内）
    import re
    broken = 0
    for md in root.rglob("*.md"):
        for m in re.finditer(r"(?<![!\w])\[\[([^\]#|]+)", md.read_text(encoding="utf-8", errors="ignore")):
            target = m.group(1).strip()
            if not list(root.rglob(target + ".md")):
                broken += 1
    r.add("L2", "内部双链完整性", "PASS" if broken == 0 else "WARNING", f"{broken} 个未解析目标")

    # L3 Security
    pol = root / "SYSTEM" / "policy.yaml"
    r.add("L3", "策略文件 policy.yaml", "PASS" if pol.exists() else "NOT CHECKED",
          "存在（仅检查存在性；真实权限由外部权限层执行）" if pol.exists() else "未配置，本 Skill 不判定为通过")
    grant = list(root.rglob("*GRANT*.json"))
    expired = 0
    for g in grant:
        try:
            import json, datetime
            d = json.loads(g.read_text(encoding="utf-8"))
            exp = d.get("expires_at", "")
            if exp and datetime.datetime.fromisoformat(exp) < datetime.datetime.now():
                expired += 1
        except Exception:
            expired += 1
    r.add("L3", "授权凭据有效性", "PASS" if grant and expired == 0 else ("WARNING" if grant else "NOT CHECKED"),
          f"{len(grant)} 份凭据，{expired} 份过期/损坏")
    # 敏感信息粗检
    secret_hits = 0
    for md in root.rglob("*.md"):
        t = md.read_text(encoding="utf-8", errors="ignore")
        if "github_pat_" in t or "-----BEGIN" in t:
            secret_hits += 1
    r.add("L3", "敏感信息泄露粗检", "PASS" if secret_hits == 0 else "ERROR",
          f"{secret_hits} 个文件疑似含凭证")

    # L4 Operational
    for d in ["Inbox", "Pending", "Outbox"]:
        p = root / d
        r.add("L4", f"目录 {d}/", "PASS" if p.exists() else "NOT CHECKED",
              "存在" if p.exists() else "未建立（回执/审批数据契约未启用）")
    receipts = list(root.rglob("*Receipt*.md")) + list(root.rglob("*receipt*.md"))
    r.add("L4", "Outbox Receipt 记录", "PASS" if receipts else "NOT CHECKED",
          f"{len(receipts)} 条回执" if receipts else "无回执数据，不判定通过")

    # L5 Value（本 Skill 不捏造指标）
    r.add("L5", "任务成功率", "NOT CHECKED", "需 Runtime 埋点，本 Skill 无数据")
    r.add("L5", "返工率 Rework Rate", "NOT CHECKED", "需 Runtime 埋点，本 Skill 无数据")
    r.add("L5", "维护成本", "NOT CHECKED", "需用户记录，本 Skill 不推算")
    return r
