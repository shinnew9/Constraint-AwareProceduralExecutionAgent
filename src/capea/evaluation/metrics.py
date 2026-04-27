from __future__ import annotations

from typing import Iterable, List
from capea.schemas import ValidationReport


# def constraint_violation_rate(reports: Iterable[ValidationReport]) -> float:
#     reports = list(reports)
#     if not reports:
#         return 0.0
#     violated = sum(1 for r in reports if not r.valid)
#     return violated / len(reports)

def constraint_violation_rate(results):
    total = len(results)
    violations = sum(1 for r in results if not r["success"])
    return violations / total if total > 0 else 0.0


def execution_success_rate(results: Iterable[dict]) -> float:
    results = list(results)
    if not results:
        return 0.0
    return sum(1 for r in results if r.get("success")) / len(results)


def average_makespan(results: Iterable[dict]) -> float:
    values = [r.get("makespan", 0) for r in results if r.get("success")]
    return sum(values) / len(values) if values else 0.0


def evaluate_graph(graph_data, schedule, validation_report):
    """
    Evaluate execution quality of CAPEA pipeline
    """

    # 1. semantic validity
    semantic_errors = [
        issue for issue in validation_report.get("issues", [])
        if issue.get("code") == "semantic_sanity_error"
    ]
    semantic_validity = 1.0 if len(semantic_errors) == 0 else 0.0

    # 2. resource conflicts
    resource_conflicts = 0
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            a = schedule[i]
            b = schedule[j]

            overlap = not (
                a["end_time"] <= b["start_time"]
                or b["end_time"] <= a["start_time"]
            )

            shared_resource = set(a.get("resources", [])) & set(b.get("resources", []))

            if overlap and shared_resource:
                resource_conflicts += 1

    # 3. temporal violations
    temporal_violations = 0
    schedule_map = {step["node_id"]: step for step in schedule}

    for edge in graph_data.get("edges", []):
        if isinstance(edge, dict):
            src = edge.get("source")
            dst = edge.get("target")
        else:
            src, dst = edge

        if src not in schedule_map or dst not in schedule_map:
            continue

        s_node = schedule_map[src]
        d_node = schedule_map[dst]

        if s_node["end_time"] > d_node["start_time"]:
            temporal_violations += 1

    # 4. execution success
    execution_success = (
        validation_report.get("is_valid", False)
        and resource_conflicts == 0
        and temporal_violations == 0
    )

    return {
        "semantic_validity": semantic_validity,
        "resource_conflicts": resource_conflicts,
        "temporal_violations": temporal_violations,
        "execution_success": execution_success,
    }