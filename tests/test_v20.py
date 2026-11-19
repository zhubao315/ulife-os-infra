import unittest, tempfile, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import observability_engine, orchestration_engine, evolution_engine

class TestObservability(unittest.TestCase):
    def test_metrics_defined(self):
        self.assertEqual(len(observability_engine.METRICS), 10)
    def test_no_data_not_measured(self):
        with tempfile.TemporaryDirectory() as td:
            c = observability_engine.collect(td)
            self.assertIsNone(c["task_success_rate"])  # 无回执 → None（NOT MEASURED）
    def test_from_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/"Outbox"; out.mkdir()
            (out/"r1.json").write_text(json.dumps({"result":"success"}), encoding="utf-8")
            (out/"r2.json").write_text(json.dumps({"result":"failure"}), encoding="utf-8")
            c = observability_engine.collect(td)
            self.assertEqual(c["task_success_rate"], 0.5)

class TestOrchestration(unittest.TestCase):
    def test_task_contract(self):
        t = orchestration_engine.make_task("研究方案", expected=["report.md"])
        self.assertEqual(orchestration_engine.validate(t), [])
        self.assertEqual(t["status"], "pending")
    def test_minimal_delegation(self):
        t = orchestration_engine.make_task("研究", deadline="2026-12-01")
        p = orchestration_engine.delegate(t, minimal_info=True)
        self.assertNotIn("deadline", p)  # 最小信息
    def test_result_verification(self):
        t = orchestration_engine.make_task("x", expected=["a.md","b.md"])
        r = orchestration_engine.verify_result(t, ["a.md"])
        self.assertFalse(r["passed"])
        self.assertIn("b.md", r["missing"])

class TestEvolution(unittest.TestCase):
    def test_bottlenecks_from_data(self):
        b = evolution_engine.find_bottlenecks({"ERROR":2,"NOT CHECKED":5,"PASS":10}, {})
        self.assertTrue(any(level=="P0" for level,_ in b))
    def test_snapshot_and_rollback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)/"pai"; root.mkdir(); (root/"x.md").write_text("v1", encoding="utf-8")
            snap = evolution_engine.snapshot(root, str(Path(td)/"backup"))
            (root/"x.md").write_text("v2", encoding="utf-8")
            evolution_engine.rollback(snap, root)
            self.assertEqual((root/"x.md").read_text(encoding="utf-8"), "v1")

if __name__ == "__main__":
    unittest.main()
