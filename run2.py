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

    def find_virus(position):
        dist_virus = bfs(position)
        reachable_gates = [
            gate_virus for gate_virus in gates if gate_virus in dist_virus
        ]
        if not reachable_gates:
            return None

        min_dist = min(dist_virus[gate_virus] for gate_virus in reachable_gates)
        target_gates = [
            gate_virus
            for gate_virus in reachable_gates
            if dist_virus[gate_virus] == min_dist
        ]
        target_gate = sorted(target_gates)[0]

        neighbors = sorted(graph.get(position, []))
        best_neighbor = None
        min_dist_gate = float("inf")

        for neighbor in neighbors:
            dist_neighbor = bfs(neighbor)
            if target_gate in dist_neighbor:
                distance = dist_neighbor[target_gate]
                if distance < min_dist_gate or (
                    distance == min_dist_gate
                    and (best_neighbor is None
                    or neighbor < best_neighbor)
                ):
                    min_dist_gate = distance
                    best_neighbor = neighbor

        return best_neighbor

    while True:
        next_move = find_virus(virus)
        if next_move is None:
            break

        if next_move in gates:
            possible_edges = []
            for gate in gates:
                if virus in graph.get(gate, []):
                    possible_edges.append(f"{gate}-{virus}")

            possible_edges.sort()
            if possible_edges:
                best_edge = possible_edges[0]
                result.append(best_edge)

                gate, node = best_edge.split("-")
                graph[gate].discard(node)
                graph[node].discard(gate)

                if not graph[gate]:
                    gates.remove(gate)
            else:
                break

        else:
            possible_edges = []
            for gate in gates:
                for node in graph.get(gate, []):
                    if node.islower():
                        possible_edges.append(f"{gate}-{node}")

            possible_edges.sort()
            if possible_edges:
                best_edge = possible_edges[0]
                result.append(best_edge)

                gate, node = best_edge.split("-")
                graph[gate].discard(node)
                graph[node].discard(gate)

                if not graph[gate]:
                    gates.remove(gate)
            else:
                break

        virus = next_move

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
