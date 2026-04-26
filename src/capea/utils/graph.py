from collections import defaultdict, deque
from typing import Dict, List, Iterable, Set, Tuple


def build_adjacency(edges: Iterable[Tuple[str, str]]) -> Dict[str, List[str]]:
    adj = defaultdict(list)
    for src, dst in edges:
        adj[src].append(dst)
    return dict(adj)


def topological_sort(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[str]:
    nodes = list(nodes)
    indegree = {node: 0 for node in nodes}
    adj = defaultdict(list)

    for src, dst in edges:
        adj[src].append(dst)
        indegree[dst] = indegree.get(dst, 0) + 1
        indegree.setdefault(src, 0)

    queue = deque([node for node in indegree if indegree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for nxt in adj[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(indegree):
        raise ValueError("Cycle detected in DAG.")

    return order


def has_cycle(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> bool:
    try:
        topological_sort(nodes, edges)
        return False
    except ValueError:
        return True


def ancestors(target: str, edges: Iterable[Tuple[str, str]]) -> Set[str]:
    reverse = defaultdict(list)
    for src, dst in edges:
        reverse[dst].append(src)

    seen = set()
    stack = list(reverse[target])

    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(reverse[node])

    return seen