from typing import Dict, List

from capea.schemas import ActionGraph, ScheduledStep
from capea.logic.validator import DAGValidator
from capea.utils import topological_sort


class ExecutionSimulator:
    def __init__(self, graph: ActionGraph):
        self.graph = graph
        self.node_map = graph.node_map()

    def run(self) -> Dict:
        validator = DAGValidator(self.graph)
        report = validator.validate()

        if not report.is_valid:
            return {
                "success": False,
                "issues": [issue.model_dump() for issue in report.issues],
                "schedule": []
            }

        schedule = self._schedule()

        return {
            "success": True,
            "issues": [],
            "makespan": max((step.end_time for step in schedule), default=0),
            "schedule": [step.model_dump() for step in schedule]
        }

    def _schedule(self) -> List[ScheduledStep]:
        order = topological_sort(self.graph.node_ids(), self.graph.edges)

        finish_times: Dict[str, int] = {}
        resource_available_time: Dict[str, int] = {}
        scheduled_steps: List[ScheduledStep] = []

        incoming = {node_id: [] for node_id in self.graph.node_ids()}
        for src, dst in self.graph.edges:
            incoming[dst].append(src)

        for node_id in order:
            node = self.node_map[node_id]

            dependency_ready_time = 0
            if incoming[node_id]:
                dependency_ready_time = max(finish_times[parent] for parent in incoming[node_id])

            resource_ready_time = 0
            if node.resources:
                resource_ready_time = max(
                    resource_available_time.get(resource, 0)
                    for resource in node.resources
                )

            start_time = max(dependency_ready_time, resource_ready_time)
            end_time = start_time + node.duration

            for resource in node.resources:
                resource_available_time[resource] = end_time

            finish_times[node_id] = end_time

            scheduled_steps.append(
                ScheduledStep(
                    node_id=node.id,
                    start_time=start_time,
                    end_time=end_time,
                    resources=node.resources,
                )
            )

        return scheduled_steps