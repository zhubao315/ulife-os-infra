import unittest, tempfile, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import receipt_engine, policy_engine, routing_engine, memory_engine

class TestReceipt(unittest.TestCase):
    def test_success_needs_evidence(self):
        r = receipt_engine.build_receipt("publish", "success", "")
        self.assertGreater(len(receipt_engine.validate(r)), 0)
    def test_persist_and_audit(self):
        with tempfile.TemporaryDirectory() as td:
            r = receipt_engine.build_receipt("publish", "success", "https://evidence", verified=True)
            receipt_engine.persist(td, r)
            a = receipt_engine.audit(td)
            self.assertEqual(a["count"], 1)
            self.assertEqual(a["success_without_evidence"], 0)

class TestDataPolicy(unittest.TestCase):
    def test_private_blocked(self):
        ok, msg = policy_engine.can_send_external("PRIVATE", "external_send")
        self.assertFalse(ok)
    def test_public_allowed(self):
        ok, _ = policy_engine.can_send_external("PUBLIC", "external_send")
        self.assertTrue(ok)

class TestRouting(unittest.TestCase):
    def test_private_routes_local(self):
        d = routing_engine.decide("私密内容分析", "PRIVATE")
        self.assertEqual(d["route"], "local")
    def test_cloud_task_with_private_blocked(self):
        d = routing_engine.decide("复杂架构研究", "PRIVATE")
        self.assertEqual(d["route"], "local")
        self.assertIn("blocked_reason", d)
    def test_research_cloud(self):
        d = routing_engine.decide("复杂架构研究")
        self.assertEqual(d["route"], "cloud")

class TestMemoryOps(unittest.TestCase):
    def test_backup_restore_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root/"USER/memory").mkdir(parents=True)
            m = {"id":"m1","type":"explicit_fact","content":"x","source":"conv","created_at":"2026-11-19","status":"approved"}
            (root/"USER/memory/m1.json").write_text(json.dumps(m), encoding="utf-8")
            b = Path(td)/"backup.json"
            memory_engine.backup(root, b)
            (root/"USER/memory/m1.json").unlink()
            n = memory_engine.restore(root, b, merge=True)
            self.assertEqual(n, 1)

if __name__ == "__main__":
    unittest.main()
