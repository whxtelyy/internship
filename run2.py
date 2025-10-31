import sys
from collections import deque


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
            for neigh in sorted(graph[current]):
                if neigh not in distances:
                    distances[neigh] = distances[current] + 1
                    queue.append(neigh)
        return distances

    while True:
        dist = bfs(virus)
        reachable_gates = [gate for gate in gates if gate in dist]
        if not reachable_gates:
            break

        min_dist = min(dist[gate] for gate in reachable_gates)
        target_gates = sorted(
            [gate for gate in reachable_gates if dist[gate] == min_dist]
        )
        target_gate = target_gates[0]

        dist_to_gate = bfs(target_gate)

        neighbors = sorted(
            [neighbor for neighbor in graph[target_gate] if not neighbor.isupper()]
        )
        false_neighbors = []
        for neighbor in neighbors:
            if neighbor in dist:
                false_neighbors.append(neighbor)

        if not false_neighbors:
            gates.remove(target_gate)
            continue

        node = false_neighbors[0]
        result.append(f"{target_gate}-{node}")

        graph[target_gate].remove(node)
        graph[node].remove(target_gate)

        min_step = None
        min_step_dist = float("inf")
        for to_node in sorted(graph[virus]):
            if to_node in dist_to_gate and dist_to_gate[to_node] < min_step_dist:
                min_step = to_node
                min_step_dist = dist_to_gate[to_node]

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
