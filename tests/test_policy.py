import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import policy_engine

class TestPolicy(unittest.TestCase):
    def test_grant_verify_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            g = policy_engine.grant(root, "write", "USER/identity/X.md", "abc", "alice", 30)
            self.assertTrue(policy_engine.verify(root, g["grant_id"], "abc"))
            self.assertFalse(policy_engine.verify(root, g["grant_id"], "abc"))  # 单次

    def test_wrong_diff_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            g = policy_engine.grant(root, "write", "X", "abc", "alice", 30)
            self.assertFalse(policy_engine.verify(root, g["grant_id"], "different"))

if __name__ == "__main__":
    unittest.main()
