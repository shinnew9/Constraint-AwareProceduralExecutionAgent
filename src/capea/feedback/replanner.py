from __future__ import annotations

from copy import deepcopy
from capea.schemas import ActionGraph


def replan_after_failure(graph: ActionGraph, failed_node_id: int, reason: str) -> ActionGraph:
    """Minimal skeleton: mark failed node and downstream nodes for regeneration.

    This is intentionally simple: future versions can ask the LLM to regenerate only the
    failed subgraph instead of restarting the entire parsing stage.
    """
    updated = deepcopy(graph)
    for node in updated.nodes:
        if node.id == failed_node_id:
            node.action = f"retry_{node.action}"
            node.duration += 5
    return updated
