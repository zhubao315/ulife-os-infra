"""Agent Orchestration：统一 Task Contract + 委托（最小信息）+ 结果验证。零依赖。"""
import json, uuid, datetime
from pathlib import Path

REQUIRED = ["task_id", "objective", "permissions", "expected_output", "status"]
VALID_STATUS = ["pending", "running", "done", "failed", "blocked"]

def make_task(objective, inputs=None, constraints=None, permissions=None, expected=None, deadline=None):
    return {
        "task_id": "task-" + uuid.uuid4().hex[:8],
        "objective": objective,
        "inputs": inputs or [],
        "constraints": constraints or [],
        "permissions": permissions or ["read_only"],
        "expected_output": expected or ["report.md"],
        "deadline": deadline,
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat(),
    }

def validate(task):
    errs = []
    for k in REQUIRED:
        if k not in task or task[k] in (None, ""):
            errs.append("缺字段: " + k)
    if task.get("status") not in VALID_STATUS:
        errs.append("非法 status")
    return errs

def delegate(task, minimal_info=True):
    """生成最小化委托载荷：只给完成任务所需最少信息。"""
    payload = {"task_id": task["task_id"], "objective": task["objective"],
               "inputs": task.get("inputs", []), "constraints": task.get("constraints", []),
               "permissions": task.get("permissions", []),
               "expected_output": task.get("expected_output", [])}
    if not minimal_info:
        payload["deadline"] = task.get("deadline")
    return payload

def verify_result(task, output_files):
    """结果验证：expected_output 是否全部产出。"""
    expected = set(task.get("expected_output", []))
    actual = set(str(x) for x in output_files)
    missing = expected - actual
    return {"passed": len(missing) == 0, "missing": sorted(missing)}
