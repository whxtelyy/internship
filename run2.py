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
        dist_from_virus = bfs(position)
        reachable_gates_virus = [
            gate_virus for gate_virus in gates if gate_virus in dist_from_virus
        ]
        if not reachable_gates_virus:
            return None

        min_dist_virus = min(
            dist_from_virus[gate_virus] for gate_virus in reachable_gates_virus
        )
        target_gates = [
            gate_virus
            for gate_virus in reachable_gates_virus
            if dist_from_virus[gate_virus] == min_dist_virus
        ]

        target_gate_virus = sorted(target_gates)[0]

        best_neighbor = None
        best_distance = float("inf")

        neighbors = sorted(graph.get(position, []))
        for neigh in neighbors:
            dist_neighbor = bfs(neigh)
            if target_gate_virus in dist_neighbor:
                distance = dist_neighbor[target_gate_virus]
                if distance < best_distance or (
                    distance == best_distance and neigh < best_neighbor
                ):
                    best_neighbor = neigh
                    best_distance = distance

        return best_neighbor

    while True:
        gateway = False
        possible_edges = []

        for neighbor in graph.get(virus, []):
            if neighbor in gates:
                gateway = True
                possible_edges.append(f"{neighbor}-{virus}")

        if gateway:
            possible_edges.sort()
            best_edge = possible_edges[0]
            result.append(best_edge)

            gate, node = best_edge.split("-")
            graph[gate].discard(node)
            graph[node].discard(gate)

            if not graph[node]:
                gates.remove(gate)

        else:
            dist_virus = bfs(virus)
            reachable_gates = [gate for gate in gates if gate in dist_virus]
            if not reachable_gates:
                break

            min_dist = min(dist_virus[gate] for gate in reachable_gates)
            possible_gates = [
                gate for gate in reachable_gates if dist_virus[gate] == min_dist
            ]
            target_gate = sorted(possible_gates)[0]

            possible_edges = []
            for node in sorted(graph.get(target_gate, [])):
                if node.islower():
                    possible_edges.append(f"{target_gate}-{node}")

            if not possible_edges:
                all_edges = []
                for gate in gates:
                    for node in sorted(graph.get(gate, [])):
                        if node.islower():
                            all_edges.append(f"{gate}-{node}")

                if not all_edges:
                    break

                all_edges.sort()
                best_edge = all_edges[0]
            else:
                possible_edges.sort()
                best_edge = possible_edges[0]

            result.append(best_edge)

            gate, node = best_edge.split("-")
            graph[gate].discard(node)
            graph[node].discard(gate)

            if not graph[gate]:
                gates.remove(gate)

        next_move = find_virus(virus)
        if next_move is None:
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
