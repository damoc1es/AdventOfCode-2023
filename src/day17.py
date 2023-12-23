from queue import PriorityQueue

DAY = 17

LEFT, RIGHT, UP, DOWN, NONE = (0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)
counterpart = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP, NONE: NONE}


def print_matrix(matrix: list[list]) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print()


def is_ok(matrix: list[list], i: int, j: int) -> bool:
    if i < 0 or j < 0:
        return False
    if i >= len(matrix) or j >= len(matrix[i]):
        return False
    return True


def get_possible(i: int, j: int, direction: tuple[int], min_move: int, max_move: int) -> list[tuple[int, int, tuple[int]]]:
    lst = []
    directions = {LEFT, RIGHT, UP, DOWN} - {direction} - {counterpart[direction]}
    
    for (di, dj) in directions:
        for move in range(min_move, max_move+1):
            lst.append((i+di*move, j+dj*move, (di, dj)))
    
    return lst


def visualize_path(matrix: list[list], path: list[list[dict]], i: int, j: int, state: tuple[int]):
    mat_out = [['.' for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    while state != (0, 0) and path[i][j][state]:
        mat_out[i][j] = 'X'
        i, j, state = path[i][j][state]

    mat_out[i][j] = 'X'
    print_matrix(mat_out)


def dijkstra(matrix: list[list[int]], min_move: int, max_move: int) -> int:
    dist = [[{k: float("inf") for k in (LEFT, RIGHT, UP, DOWN)} for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    path = [[{k: None for k in (LEFT, RIGHT, UP, DOWN)} for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    dist[0][0][NONE] = 0

    pq = PriorityQueue()
    pq.put((0, (0, 0, NONE)))

    in_queue = set()
    in_queue.add((0, 0, NONE))

    while pq.qsize():
        _, node = pq.get()
        i, j, state = node
        in_queue.remove((i, j, state))

        for new_node in get_possible(i, j, state, min_move, max_move):
            new_i, new_j, new_state = new_node

            if is_ok(matrix, new_i, new_j):
                S = 0
                if new_i != i:
                    if i < new_i:
                        for x in range(i+1, new_i+1):
                            S += matrix[x][j]
                    elif i > new_i:
                        for x in range(i-1, new_i-1, -1):
                            S += matrix[x][j]
                elif new_j != j:
                    if j < new_j:
                        for x in range(j+1, new_j+1):
                            S += matrix[i][x]
                    elif j > new_j:
                        for x in range(j-1, new_j-1, -1):
                            S += matrix[i][x]

                if dist[i][j][state] + S < dist[new_i][new_j][new_state]:
                    dist[new_i][new_j][new_state] = dist[i][j][state] + S
                    path[new_i][new_j][new_state] = (i, j, state)

                    if new_node not in in_queue:
                        pq.put((dist[new_i][new_j][new_state], new_node))
                        in_queue.add(new_node)

    return min(dist[-1][-1][DOWN], dist[-1][-1][RIGHT])


def part1(inp: list[str]) -> int:
    mat = [[int(c) for c in row] for row in inp]
    return dijkstra(mat, 1, 3)


def part2(inp: list[str]) -> int:
    mat = [[int(c) for c in row] for row in inp]
    return dijkstra(mat, 4, 10)


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
