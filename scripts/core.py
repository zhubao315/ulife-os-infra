"""公共工具：安全路径、canonical 模板定位、报告模型。零第三方依赖。"""
from pathlib import Path
import re, json, hashlib

TELOS = ["MISSION", "GOALS", "PROJECTS", "BELIEFS", "MODELS",
         "STRATEGIES", "NARRATIVES", "LEARNED", "CHALLENGES", "IDEAS"]
PROFILES = {
    "starter": ["MISSION", "GOALS", "PROJECTS"],           # + BOUNDARIES 由 init 注入
    "standard": TELOS,
    "advanced": TELOS,
}
CANON = Path(__file__).resolve().parent.parent  # 技能包根

def safe_join(root: Path, rel: str) -> Path:
    """防路径穿越与危险链接：rel 必须保持为 root 下普通文件。
    逐级检查每一段是否为 symlink（含指向 root 自身的链接），再检查解析后越界。"""
    root_r = root.resolve()
    cur = root_r
    for part in Path(rel).parts:
        if part in (".", ""):
            continue
        cur = cur / part
        if cur.is_symlink():
            raise ValueError(f"拒绝符号链接: {rel}（段 {part}）")
    target = (root_r / rel).resolve()
    if not str(target).startswith(str(root_r) + "/") and target != root_r:
        raise ValueError(f"路径越界: {rel}")
    return target

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def strip_fm(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end+5:]
    return text

def parse_fm(text: str) -> dict:
    """极简 FM 解析（够用即可，不依赖 yaml）。"""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.+)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"\'')
    return fm

class Report:
    def __init__(self):
        self.items = []  # dict: layer, check, status, detail
    def add(self, layer, check, status, detail=""):
        assert status in ("PASS", "WARNING", "ERROR", "NOT CHECKED")
        self.items.append(dict(layer=layer, check=check, status=status, detail=detail))
    def counts(self):
        c = {k: 0 for k in ("PASS", "WARNING", "ERROR", "NOT CHECKED")}
        for i in self.items:
            c[i["status"]] += 1
        return c
    def to_json(self):
        return json.dumps({"counts": self.counts(), "items": self.items}, ensure_ascii=False, indent=2)
    def to_md(self, root):
        c = self.counts()
        out = [f"# 审计报告 — {root}", "",
               f"PASS {c['PASS']} · WARNING {c['WARNING']} · ERROR {c['ERROR']} · NOT CHECKED {c['NOT CHECKED']}", "",
               "| 层 | 检查 | 状态 | 说明 |", "|---|---|---|---|"]
        for i in self.items:
            out.append(f"| {i['layer']} | {i['check']} | {i['status']} | {i['detail']} |")
        return "\n".join(out) + "\n"
