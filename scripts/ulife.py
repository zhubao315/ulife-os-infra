#!/usr/bin/env python3
"""uLife OS Infra 统一 CLI — 零第三方依赖。
用法：
  python scripts/ulife.py init --target ./my-ulife --profile starter [--dry-run]
  python scripts/ulife.py audit --target ./my-ulife [--format json|md]
  python scripts/ulife.py doctor --target ./my-ulife
  python scripts/ulife.py grant --target ./my-ulife --op write --file USER/identity/X.md --diff <hash> --approver <name>
  python scripts/ulife.py verify --target ./my-ulife --grant <id> --diff <hash>
"""
import argparse, sys
from pathlib import Path
import init_engine, audit_engine, policy_engine

def main():
    ap = argparse.ArgumentParser(description="uLife OS Infra CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--target", default="./my-ulife")
    p.add_argument("--profile", default="starter", choices=["starter", "standard", "advanced"])
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("audit")
    p.add_argument("--target", default=".")
    p.add_argument("--format", default="md", choices=["md", "json"])
    p.add_argument("--profile", default=None, choices=["starter", "standard", "advanced"])

    p = sub.add_parser("doctor")
    p.add_argument("--target", default=".")
    p.add_argument("--profile", default=None, choices=["starter", "standard", "advanced"])

    p = sub.add_parser("grant")
    p.add_argument("--target", default=".")
    p.add_argument("--op", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--diff", required=True)
    p.add_argument("--approver", required=True)
    p.add_argument("--minutes", type=int, default=30)

    p = sub.add_parser("verify")
    p.add_argument("--target", default=".")
    p.add_argument("--grant", required=True)
    p.add_argument("--diff", required=True)

    args = ap.parse_args()
    root = Path(args.target)

    # 档位解析：显式参数 > INIT_RECEIPT.json > 默认 standard
    import json
    def resolve_profile():
        if getattr(args, "profile", None):
            return args.profile
        receipt = root / "INIT_RECEIPT.json"
        if receipt.exists():
            try:
                return json.loads(receipt.read_text(encoding="utf-8")).get("profile", "standard")
            except Exception:
                pass
        return "standard"

    if args.cmd == "init":
        init_engine.execute(root, args.profile, args.dry_run, False)
    elif args.cmd == "audit":
        r = audit_engine.run(root, resolve_profile())
        if args.format == "json":
            print(r.to_json())
        else:
            print(r.to_md(root))
        c = r.counts()
        sys.exit(1 if c["ERROR"] else 0)
    elif args.cmd == "doctor":
        r = audit_engine.run(root, resolve_profile())
        c = r.counts()
        print(f"Doctor: PASS={c['PASS']} WARN={c['WARNING']} ERR={c['ERROR']} NOTCHECKED={c['NOT CHECKED']}")
        sys.exit(1 if c["ERROR"] else 0)
    elif args.cmd == "grant":
        g = policy_engine.grant(root, args.op, args.file, args.diff, args.approver, args.minutes)
        print(f"授权凭据已生成: {g['grant_id']}（有效期 {args.minutes} 分钟，单次使用）")
    elif args.cmd == "verify":
        ok = policy_engine.verify(root, args.grant, args.diff)
        print("授权有效，已消费并记回执" if ok else "授权无效/过期/Diff 不匹配")
        sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
