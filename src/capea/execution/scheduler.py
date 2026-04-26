from __future__ import annotations

from typing import Dict, List
import networkx as nx

from capea.schemas import ActionGraph, ScheduledStep
from capea.logic.domain_rules import infer_resource


def schedule_graph(action_graph: ActionGraph) -> List[ScheduledStep]:
    """Earliest-start scheduler with dependency and resource locking."""
    G = nx.DiGraph()
    nodes = {node.id: node for node in action_graph.nodes}

    for node in action_graph.nodes:
        G.add_node(node.id)
        for dep in node.depends_on:
            G.add_edge(dep, node.id)

    resource_free_at: Dict[str, int] = {}
    end_times: Dict[int, int] = {}
    output: List[ScheduledStep] = []

    for node_id in nx.topological_sort(G):
        node = nodes[node_id]
        resource = infer_resource(node.action, node.resource)
        dep_ready = max([end_times.get(dep, 0) for dep in G.predecessors(node_id)] + [0])
        res_ready = resource_free_at.get(resource, 0)
        start = max(dep_ready, res_ready)
        end = start + node.duration

        end_times[node_id] = end
        resource_free_at[resource] = end
        output.append(ScheduledStep(
            id=node.id,
            action=node.action,
            target=node.target,
            start=start,
            end=end,
            resource=resource,
            depends_on=list(node.depends_on),
        ))
    return output
