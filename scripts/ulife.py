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
import init_engine, audit_engine, policy_engine, memory_engine, integrate_engine, budget_engine, receipt_engine, routing_engine, observability_engine, orchestration_engine, evolution_engine

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

    p = sub.add_parser("memory-lint")
    p.add_argument("--target", default=".")

    p = sub.add_parser("integrate")
    p.add_argument("--target", default=".")
    p.add_argument("--discover", action="store_true", help="只输出发现到的资产 JSON")

    p = sub.add_parser("budget")
    p.add_argument("--window", type=int, default=200000)
    p.add_argument("--system", type=int, default=4000)
    p.add_argument("--tools", type=int, default=8000)
    p.add_argument("--tier", default="t2", choices=["t1", "t2", "t3"])

    p = sub.add_parser("route")
    p.add_argument("--task", required=True)
    p.add_argument("--level", choices=["PUBLIC","INTERNAL","PRIVATE","RESTRICTED"])

    p = sub.add_parser("receipt")
    p.add_argument("--target", default=".")
    p.add_argument("--action", required=True)
    p.add_argument("--result", required=True, choices=["success","failure","partial"])
    p.add_argument("--evidence", default="")
    p.add_argument("--approver", default="")

    p = sub.add_parser("memory-backup")
    p.add_argument("--target", default=".")
    p.add_argument("--out", required=True)

    p = sub.add_parser("memory-restore")
    p.add_argument("--target", default=".")
    p.add_argument("--backup", required=True)

    p = sub.add_parser("observe")
    p.add_argument("--target", default=".")
    p.add_argument("--format", default="md", choices=["md", "json"])

    p = sub.add_parser("task")
    p.add_argument("--action", choices=["new", "validate", "verify"], required=True)
    p.add_argument("--objective", default="")
    p.add_argument("--task-file", default="")
    p.add_argument("--outputs", nargs="*", default=[])

    p = sub.add_parser("evolve")
    p.add_argument("--action", choices=["bottlenecks", "snapshot", "rollback"], required=True)
    p.add_argument("--target", default=".")
    p.add_argument("--backup", default="")

    args = ap.parse_args()
    root = Path(getattr(args, "target", "."))

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

    elif args.cmd == "memory-lint":
        r = memory_engine.lint(root)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(1 if r["errors"] else 0)
    elif args.cmd == "integrate":
        if args.discover:
            print(json.dumps(integrate_engine.discover(root), ensure_ascii=False, indent=2))
        else:
            print(integrate_engine.propose(root))
    elif args.cmd == "budget":
        eff = budget_engine.effective_budget(args.window, args.system, args.tools)
        print(json.dumps({"window": args.window, "system": args.system, "tools": args.tools,
                          "effective_budget": eff, "tier": args.tier,
                          "tier_budget": budget_engine.tier_budget(eff, args.tier)}, indent=2))

    elif args.cmd == "route":
        print(json.dumps(routing_engine.decide(args.task, args.level), ensure_ascii=False, indent=2))
    elif args.cmd == "receipt":
        r = receipt_engine.build_receipt(args.action, args.result, args.evidence, approver=args.approver)
        errs = receipt_engine.validate(r)
        if errs:
            print("回执校验失败:", errs)
            sys.exit(1)
        receipt_engine.persist(root, r)
        print("回执已落盘:", r["receipt_id"])
    elif args.cmd == "memory-backup":
        snap = memory_engine.backup(root, args.out)
        print("备份完成:", snap["count"], "条记忆 ->", args.out)
    elif args.cmd == "memory-restore":
        n = memory_engine.restore(root, args.backup, merge=True)
        print("恢复完成:", n, "条（merge 模式，不覆盖现有）")

    elif args.cmd == "observe":
        if args.format == "json":
            print(json.dumps(observability_engine.collect(root), ensure_ascii=False, indent=2))
        else:
            print(observability_engine.report(root))
    elif args.cmd == "task":
        if args.action == "new":
            task = orchestration_engine.make_task(args.objective)
            print(json.dumps(task, ensure_ascii=False, indent=2))
        elif args.action == "validate":
            task = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
            errs = orchestration_engine.validate(task)
            print("合法" if not errs else "错误: " + "; ".join(errs))
            sys.exit(1 if errs else 0)
        elif args.action == "verify":
            task = json.loads(Path(args.task_file).read_text(encoding="utf-8"))
            print(json.dumps(orchestration_engine.verify_result(task, args.outputs), ensure_ascii=False))
    elif args.cmd == "evolve":
        if args.action == "bottlenecks":
            r = audit_engine.run(root, resolve_profile())
            obs = observability_engine.collect(root)
            for level, msg in evolution_engine.find_bottlenecks(r.counts(), obs):
                print(f"[{level}] {msg}")
        elif args.action == "snapshot":
            print("快照:", evolution_engine.snapshot(root, args.backup or (str(root) + "-backup")))
        elif args.action == "rollback":
            evolution_engine.rollback(args.backup, root)
            print("已从快照回滚")

if __name__ == "__main__":
    main()
