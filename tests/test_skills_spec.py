import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

ROOT = Path(__file__).resolve().parents[1]

class TestSkillsSpec(unittest.TestCase):
    def test_frontmatter_core_fields(self):
        sk = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(sk.startswith("---\n"))
        self.assertIn("name: ulife-os-infra", sk)
        self.assertIn("description:", sk)
        self.assertIn("license:", sk)  # 顶层可选字段（带/不带引号均合规）

    def test_progressive_disclosure_files(self):
        for f in ["references/telos.md","references/memory.md","references/skills.md",
                  "references/protocols.md","references/permissions.md","references/maintenance.md"]:
            self.assertTrue((ROOT / f).exists(), f)

    def test_skill_md_under_500(self):
        self.assertLess(len((ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()), 500)

if __name__ == "__main__":
    unittest.main()
