from __future__ import annotations

from typing import Dict, List

from capea.schemas import ActionGraph, ScheduledStep
from capea.execution.scheduler import schedule_graph
from capea.logic.validator import DAGValidator


class ExecutionSimulator:
    """Runs a lightweight feasibility simulation over the scheduled plan."""

    def __init__(self, graph: ActionGraph):
        self.graph = graph
        self.object_states: Dict[str, str] = {}

    def run(self) -> dict:
        validator = DAGValidator(self.graph)
        graph_report = validator.validate_graph()
        if not graph_report.valid:
            return {"success": False, "stage": "graph_validation", "issues": graph_report.issues, "schedule": []}

        schedule = schedule_graph(self.graph)
        schedule_report = validator.validate_schedule(schedule)
        return {
            "success": schedule_report.valid,
            "stage": "schedule_validation",
            "issues": schedule_report.issues,
            "schedule": schedule,
            "makespan": max((s.end for s in schedule), default=0),
        }
