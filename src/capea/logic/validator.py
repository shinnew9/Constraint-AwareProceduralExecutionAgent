from __future__ import annotations

from typing import Dict, List, Set
import networkx as nx

from capea.schemas import ActionGraph, ScheduledStep, ValidationIssue, ValidationReport
from capea.logic.domain_rules import is_semantically_valid


class DAGValidator:
    """Validates graph structure, semantic sanity, resources, and scheduled outputs."""

    def __init__(self, graph: ActionGraph):
        self.graph = graph
        self.nodes = {n.id: n for n in graph.nodes}

    def validate_graph(self) -> ValidationReport:
        issues: List[ValidationIssue] = []
        ids = [n.id for n in self.graph.nodes]

        if len(ids) != len(set(ids)):
            issues.append(ValidationIssue(level="error", code="DUPLICATE_ID", message="Duplicate node IDs found."))

        for node in self.graph.nodes:
            if not is_semantically_valid(node.action, node.target):
                issues.append(ValidationIssue(
                    level="error",
                    code="SEMANTIC_SANITY_FAIL",
                    node_id=node.id,
                    message=f"Nonsense action-target pair: {node.action} {node.target}",
                ))
            for dep in node.depends_on:
                if dep not in self.nodes:
                    issues.append(ValidationIssue(
                        level="error",
                        code="MISSING_DEPENDENCY",
                        node_id=node.id,
                        message=f"Node {node.id} depends on missing node {dep}.",
                    ))

        G = self._to_networkx()
        if not nx.is_directed_acyclic_graph(G):
            issues.append(ValidationIssue(level="error", code="CYCLE", message="Action graph contains a cycle."))

        return ValidationReport(valid=not any(i.level == "error" for i in issues), issues=issues)

    def validate_schedule(self, schedule: List[ScheduledStep]) -> ValidationReport:
        issues: List[ValidationIssue] = []
        by_id = {s.id: s for s in schedule}

        # Dependency order check
        for step in schedule:
            node = self.nodes.get(step.id)
            if not node:
                continue
            for dep_id in node.depends_on:
                dep = by_id.get(dep_id)
                if dep and dep.end > step.start:
                    issues.append(ValidationIssue(
                        level="error",
                        code="DEPENDENCY_VIOLATION",
                        node_id=step.id,
                        message=f"Step {step.id} starts before dependency {dep_id} finishes.",
                    ))

        # Resource overlap check
        resource_to_steps: Dict[str, List[ScheduledStep]] = {}
        for step in schedule:
            resource_to_steps.setdefault(step.resource, []).append(step)

        for resource, steps in resource_to_steps.items():
            ordered = sorted(steps, key=lambda s: s.start)
            for prev, curr in zip(ordered, ordered[1:]):
                if curr.start < prev.end:
                    issues.append(ValidationIssue(
                        level="error",
                        code="RESOURCE_CONFLICT",
                        node_id=curr.id,
                        message=f"Resource {resource} overlaps between step {prev.id} and {curr.id}.",
                    ))

        return ValidationReport(valid=not any(i.level == "error" for i in issues), issues=issues)

    def _to_networkx(self) -> nx.DiGraph:
        G = nx.DiGraph()
        for node in self.graph.nodes:
            G.add_node(node.id)
            for dep in node.depends_on:
                G.add_edge(dep, node.id)
        return G
