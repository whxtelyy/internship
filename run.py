import heapq
import sys

energy = {"A": 1, "B": 10, "C": 100, "D": 1000}
rooms_positions = {"A": 2, "B": 4, "C": 6, "D": 8}
hall_positions = [0, 1, 3, 5, 7, 9, 10]


def parse_input(lines: list) -> tuple:
    hallway = tuple(lines[1][1:-1])
    rooms = []
    for cols in [3, 5, 7, 9]:
        room = tuple(lines[number][cols] for number in range(2, len(lines) - 1))
        rooms.append(room)
    return tuple(hallway), tuple(rooms)


def is_finished(rooms: list) -> bool:
    for index, room in enumerate(rooms):
        typ = "ABCD"[index]
        if any(symbol != typ for symbol in room):
            return False
    return True


def heuristic(state: tuple) -> float:
    hallway, rooms = state
    min_energy = 0
    for index, symbol in enumerate(hallway):
        if symbol != ".":
            target_pos = rooms_positions[symbol]
            min_energy += abs(target_pos - index) * energy[symbol]
    for room_index, room in enumerate(rooms):
        target_type = "ABCD"[room_index]
        for depth, symbol in enumerate(room):
            if symbol != "." and symbol != target_type:
                target_pos = rooms_positions[symbol]
                min_energy += (
                    abs(target_pos - rooms_positions[target_type]) + depth + 1
                ) * energy[symbol]
    return min_energy


def moves(state: tuple):
    hallway, rooms = state
    for room_index, room in enumerate(rooms):
        for depth, symbol in enumerate(room):
            if symbol != ".":
                break
        else:
            continue
        target_type = "ABCD"[room_index]
        if symbol == target_type and all(
            element == target_type for element in room[depth:]
        ):
            continue
        room_pos = 2 + room_index * 2
        for hall in hall_positions:
            step = 1 if hall > room_pos else -1
            path_clear = True
            for position in range(room_pos + step, hall + step, step):
                if hallway[position] != ".":
                    path_clear = False
                    break
            if path_clear:
                new_hall = list(hallway)
                new_hall[hall] = symbol
                new_room = [list(room) for room in rooms]
                new_room[room_index][depth] = "."
                cost = (abs(hall - room_pos) + depth + 1) * energy[symbol]
                yield tuple(new_hall), tuple(tuple(room) for room in new_room), cost

    for hall_index, symbol in enumerate(hallway):
        if symbol == ".":
            continue
        room_index = "ABCD".index(symbol)
        target_room = rooms[room_index]
        if any(element != "." and element != symbol for element in target_room):
            continue
        for depth in reversed(range(len(target_room))):
            if target_room[depth] == ".":
                break
        else:
            continue
        room_pos = rooms_positions[symbol]
        step = 1 if room_pos > hall_index else -1
        path_clear = True
        for position in range(hall_index + step, room_pos + step, step):
            if hallway[position] != ".":
                path_clear = False
                break
        if path_clear:
            new_hall = list(hallway)
            new_hall[hall_index] = "."
            new_room = [list(room) for room in rooms]
            new_room[room_index][depth] = symbol
            cost = (abs(hall_index - room_pos) + depth + 1) * energy[symbol]
            yield tuple(new_hall), tuple(tuple(room) for room in new_room), cost


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    # TODO: Реализация алгоритма

    start = parse_input(lines)
    visited = {}
    pq = [(heuristic(start), 0, start)]

    while pq:
        f, cost, state = heapq.heappop(pq)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        if is_finished(state[1]):
            return cost
        for nh, nr, move_cost in moves(state):
            new_state = (nh, nr)
            new_cost = cost + move_cost
            if new_state in visited and visited[new_state] <= new_cost:
                continue
            heapq.heappush(pq, (new_cost + heuristic(new_state), new_cost, new_state))
    return 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip("\n"))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
