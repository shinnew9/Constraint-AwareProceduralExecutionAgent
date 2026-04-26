from typing import List

from capea.schemas import ActionGraph, ValidationIssue, ValidationReport
from capea.utils import has_cycle


INVALID_ACTION_TARGETS = {
    ("boil", "knife"),
    ("cut", "water"),
    ("chop", "water"),
    ("fry", "knife"),
}


class DAGValidator:
    def __init__(self, graph: ActionGraph):
        self.graph = graph
        self.node_ids = set(graph.node_ids())
        self.node_map = graph.node_map()

    def validate(self) -> ValidationReport:
        report = ValidationReport(is_valid=True)

        self._check_duplicate_node_ids(report)
        self._check_missing_edge_nodes(report)
        self._check_cycles(report)
        self._check_durations(report)
        self._check_semantic_sanity(report)

        return report

    def _check_duplicate_node_ids(self, report: ValidationReport) -> None:
        ids = self.graph.node_ids()
        duplicates = sorted({node_id for node_id in ids if ids.count(node_id) > 1})

        for node_id in duplicates:
            report.add_issue(
                ValidationIssue(
                    level="error",
                    code="duplicate_node_id",
                    message=f"Duplicate node id found: {node_id}",
                    node_id=node_id,
                )
            )

    def _check_missing_edge_nodes(self, report: ValidationReport) -> None:
        for src, dst in self.graph.edges:
            if src not in self.node_ids:
                report.add_issue(
                    ValidationIssue(
                        level="error",
                        code="missing_edge_source",
                        message=f"Edge source node does not exist: {src}",
                        node_id=src,
                    )
                )

            if dst not in self.node_ids:
                report.add_issue(
                    ValidationIssue(
                        level="error",
                        code="missing_edge_target",
                        message=f"Edge target node does not exist: {dst}",
                        node_id=dst,
                    )
                )

    def _check_cycles(self, report: ValidationReport) -> None:
        if has_cycle(self.graph.node_ids(), self.graph.edges):
            report.add_issue(
                ValidationIssue(
                    level="error",
                    code="cycle_detected",
                    message="The action graph contains a cycle, so it is not a valid DAG.",
                )
            )

    def _check_durations(self, report: ValidationReport) -> None:
        for node in self.graph.nodes:
            if node.duration <= 0:
                report.add_issue(
                    ValidationIssue(
                        level="error",
                        code="invalid_duration",
                        message=f"Node duration must be positive, got {node.duration}.",
                        node_id=node.id,
                    )
                )

    def _check_semantic_sanity(self, report: ValidationReport) -> None:
        for node in self.graph.nodes:
            pair = (node.action.lower(), node.target.lower())
            if pair in INVALID_ACTION_TARGETS:
                report.add_issue(
                    ValidationIssue(
                        level="error",
                        code="semantic_sanity_error",
                        message=f"Invalid action-target pair: {node.action} {node.target}",
                        node_id=node.id,
                    )
                )