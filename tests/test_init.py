import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import init_engine

class TestInit(unittest.TestCase):
    def test_starter_uses_canonical_templates(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            r = init_engine.execute(root, "starter", False, False)
            self.assertEqual(r["profile"], "starter")
            mission = (root / "TELOS" / "MISSION.md").read_text(encoding="utf-8")
            self.assertIn("hint:", mission)  # canonical 模板带 hint，证明未自造
            self.assertIn("BOUNDARIES.md", [x.name for x in (root/"TELOS").glob("*")])

    def test_idempotent_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_engine.execute(root, "starter", False, False)
            p = root / "TELOS" / "MISSION.md"
            p.write_text("USER CUSTOM", encoding="utf-8")
            r = init_engine.execute(root, "starter", False, False)
            self.assertIn("TELOS/MISSION.md", r["kept_user_files"])
            self.assertEqual(p.read_text(encoding="utf-8"), "USER CUSTOM")

    def test_dry_run_no_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            r = init_engine.execute(root, "starter", True, False)
            self.assertTrue(r["dry_run"])
            self.assertFalse((root / "TELOS").exists())

if __name__ == "__main__":
    unittest.main()
