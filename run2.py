import sys
from collections import deque
from importlib.metadata import packages_distributions


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    graph = {}
    for node1, node2 in edges:
        graph.setdefault(node1, set()).add(node2)
        graph.setdefault(node2, set()).add(node1)
    for node in graph:
        graph[node] = sorted(graph[node])

    gates = sorted([node for node in graph if node.isupper()])
    virus = "a"
    result = []

    def bfs(start: str) -> dict[str, int]:
        distances = {start: 0}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neigh in graph.get(current, []):
                if neigh not in distances:
                    distances[neigh] = distances[current] + 1
                    queue.append(neigh)
        return distances

    def bfs_parent(start: str):
        distances = {start: 0}
        parent = {}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neigh in graph.get(current, []):
                if neigh not in distances:
                    distances[neigh] = distances[current] + 1
                    parent[neigh] = current
                    queue.append(neigh)
        return distances, parent

    while True:
        dist, parent = bfs_parent(virus)
        reachable_gates = [gate for gate in gates if gate in dist and graph.get(gate)]
        if not reachable_gates:
            break

        min_dist = min(dist[gate] for gate in reachable_gates)
        target_gates = sorted(
            [gate for gate in reachable_gates if dist[gate] == min_dist]
        )
        target_gate = target_gates[0]

        prev_node = parent.get(target_gate)
        if prev_node is None:
            neighbors = sorted(
                [neighbor for neighbor in graph.get(target_gate, []) if neighbor.isupper()]
            )
            if not neighbors:
                if target_gate in gates:
                    gates.remove(target_gate)
                continue
            node = neighbors[0]
        else:
            node = prev_node


        result.append(f"{target_gate}-{node}")

        if node in graph.get(target_gate, []):
            graph[target_gate].remove(node)
        if target_gate in graph.get(node, []):
            graph[node].remove(target_gate)

        if not graph.get(target_gate):
            if target_gate in gates:
                gates.remove(target_gate)

        dist_to_node = bfs(virus)

        reachable_gates_to_node = [gate for gate in gates
                                   if gate in dist_to_node and graph.get(gate)]
        if not reachable_gates_to_node:
            break

        min_dist2 = min(
            dist_to_node[gate] for gate in reachable_gates_to_node
        )
        target_gates2 = sorted(
            [gate for gate in reachable_gates_to_node
             if dist_to_node[gate] == min_dist2]
        )
        target_gate_to_node = target_gates2[0]

        gate_dist = bfs(target_gate_to_node)

        min_step = None
        min_step_dist = float("inf")
        for to_node in sorted(graph.get(virus, [])):
            if to_node in gate_dist and gate_dist[to_node] < min_step_dist:
                min_step = to_node
                min_step_dist = gate_dist[to_node]

        if min_step is None:
            break

        virus = min_step

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition("-")
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()