import unittest, tempfile, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import budget_engine, memory_engine, integrate_engine

class TestBudget(unittest.TestCase):
    def test_effective_budget(self):
        e = budget_engine.effective_budget(200000, 4000, 8000)
        self.assertLess(e, 200000 - 4000 - 8000)
        self.assertGreater(e, 0)
    def test_tier_scaling(self):
        e = budget_engine.effective_budget(200000, 4000, 8000)
        self.assertLess(budget_engine.tier_budget(e, "t1"), budget_engine.tier_budget(e, "t3"))

class TestMemory(unittest.TestCase):
    def test_validate_ok(self):
        m = {"id":"m1","type":"explicit_fact","content":"用户偏好简洁","source":"conversation",
             "created_at":"2026-11-19","status":"approved","sensitivity":"PRIVATE"}
        self.assertEqual(memory_engine.validate(m), [])
    def test_inference_not_fact(self):
        m = {"id":"m2","type":"explicit_fact","content":"maybe","source":"inference",
             "created_at":"2026-11-19","status":"captured"}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root/"USER/memory").mkdir(parents=True)
            (root/"USER/memory/m2.json").write_text(json.dumps(m), encoding="utf-8")
            r = memory_engine.lint(root)
            self.assertTrue(any("推断" in str(e) for _, e in r["errors"]))
    def test_conflict_detection(self):
        a = {"id":"a","type":"semantic","content":"python 简洁 结构化"}
        b = {"id":"b","type":"semantic","content":"python 结构化 类型"}
        c = memory_engine.detect_conflicts([a,b])
        self.assertGreater(len(c), 0)

class TestIntegrate(unittest.TestCase):
    def test_discover(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root/".obsidian").mkdir()
            (root/"CLAUDE.md").write_text("x", encoding="utf-8")
            d = integrate_engine.discover(root)
            self.assertGreater(len(d["claude_md"]), 0)
    def test_propose_no_parallel_system(self):
        with tempfile.TemporaryDirectory() as td:
            p = integrate_engine.propose(Path(td))
            self.assertIn("禁止", p)

if __name__ == "__main__":
    unittest.main()
