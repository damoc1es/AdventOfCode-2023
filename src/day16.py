from queue import Queue

DAY = 16

RIGHT, LEFT, UP, DOWN = 1, 2, 3, 4


def is_ok(mat: list[list], x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return False
    if x >= len(mat) or y >= len(mat[x]):
        return False
    return True


def queue_add(q: Queue, energy: list[list[tuple]], x: int, y: int, direction: int) -> None:
    if is_ok(energy, x, y) and direction not in energy[x][y]:
        q.put((x, y, direction))


def get_energized(mat: list[list[str]], start_point: tuple[int], direction: int) -> int:
    energy = [[() for _ in row] for row in mat]
    
    q = Queue()
    q.put((start_point[0], start_point[1], direction))
    while not q.empty():
        x, y, direction = q.get()

        while is_ok(mat, x, y):
            if direction in energy[x][y]:
                break
            energy[x][y] += (direction,)

            leave = False
            if direction == RIGHT:
                if mat[x][y] in ('.', '-'):
                    y += 1
                else:
                    if mat[x][y] in ('/', '|'):
                        queue_add(q, energy, x-1, y, UP)
                    if mat[x][y] in ('\\', '|'):
                        queue_add(q, energy, x+1, y, DOWN)
                    leave = True
            elif direction == LEFT:
                if mat[x][y] in ('.', '-'):
                    y -= 1
                else:
                    if mat[x][y] in ('/', '|'):
                        queue_add(q, energy, x+1, y, DOWN)
                    if mat[x][y] in ('\\', '|'):
                        queue_add(q, energy, x-1, y, UP)
                    leave = True
            elif direction == UP:
                if mat[x][y] in ('.', '|'):
                    x -= 1
                else:
                    if mat[x][y] in ('/', '-'):
                        queue_add(q, energy, x, y+1, RIGHT)
                    if mat[x][y] in ('\\', '-'):
                        queue_add(q, energy, x, y-1, LEFT)
                    leave = True
            elif direction == DOWN:
                if mat[x][y] in ('.', '|'):
                    x += 1
                else:
                    if mat[x][y] in ('/', '-'):
                        queue_add(q, energy, x, y-1, LEFT)
                    if mat[x][y] in ('\\', '-'):
                        queue_add(q, energy, x, y+1, RIGHT)
                    leave = True
            if leave == True:
                break
    
    k = 0
    for i in range(len(energy)):
        for j in range(len(energy[i])):
            if energy[i][j] != ():
                k += 1
    
    return k


def part1(inp: list[str]) -> int:
    mat = [list(row) for row in inp]
    return get_energized(mat, (0, 0), RIGHT)


def part2(inp: list[str]) -> int:
    mat = [list(row) for row in inp]
    max_energy = -1

    for i in range(len(mat)):
        max_energy = max(max_energy, get_energized(mat, (i, 0), RIGHT))
        max_energy = max(max_energy, get_energized(mat, (i, len(mat[i])-1), LEFT))

    for j in range(len(mat[0])):
        max_energy = max(max_energy, get_energized(mat, (0, j), DOWN))
        max_energy = max(max_energy, get_energized(mat, (len(mat)-1, j), UP))
    
    return max_energy


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
