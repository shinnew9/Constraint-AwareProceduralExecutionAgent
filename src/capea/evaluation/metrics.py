from __future__ import annotations

from typing import Iterable, List
from capea.schemas import ValidationReport


def constraint_violation_rate(reports: Iterable[ValidationReport]) -> float:
    reports = list(reports)
    if not reports:
        return 0.0
    violated = sum(1 for r in reports if not r.valid)
    return violated / len(reports)


def execution_success_rate(results: Iterable[dict]) -> float:
    results = list(results)
    if not results:
        return 0.0
    return sum(1 for r in results if r.get("success")) / len(results)


def average_makespan(results: Iterable[dict]) -> float:
    values = [r.get("makespan", 0) for r in results if r.get("success")]
    return sum(values) / len(values) if values else 0.0
