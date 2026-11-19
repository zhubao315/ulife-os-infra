import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import init_engine, audit_engine

class TestAudit(unittest.TestCase):
    def test_starter_profile_no_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_engine.execute(root, "starter", False, False)
            r = audit_engine.run(root, "starter")
            self.assertEqual(r.counts()["ERROR"], 0)
            self.assertGreater(r.counts()["PASS"], 0)

    def test_standard_profile_reports_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_engine.execute(root, "starter", False, False)
            r = audit_engine.run(root, "standard")
            self.assertGreater(r.counts()["ERROR"], 0)  # 缺 7 个 TELOS

    def test_not_checked_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            r = audit_engine.run(root, "standard")
            self.assertGreater(r.counts()["NOT CHECKED"], 0)  # 不默认通过

if __name__ == "__main__":
    unittest.main()
