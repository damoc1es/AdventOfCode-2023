import numpy as np
from queue import Queue

DAY = 21

encode = {'.': 0, '#': -2, 'S': 1}
di = (0, 0, 1, -1)
dj = (1, -1, 0, 0)


def is_ok(i: int, j: int, map: list[list]) -> bool:
    return 0 <= i < len(map) and 0 <= j < len(map[0])


def Lee(map: list[list], start: tuple[int], max_step: int) -> None:
    Q = Queue()
    Q.put(start)

    while not Q.empty():
        i, j = Q.get()
        
        for d in range(4):
            i_next, j_next = i+di[d], j+dj[d]

            if is_ok(i_next, j_next, map) and map[i_next][j_next] == encode['.'] and map[i][j] < max_step:
                map[i_next][j_next] = map[i][j] + 1
                Q.put((i_next, j_next))


def part1(inp: list[str]) -> int:
    mat = []
    for line in inp:
        mat.append([encode[x] for x in line])
    step = 64

    start = (len(mat)//2, len(mat)//2)
    
    Lee(mat, start, step)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == step:
                
                for d in range(4):
                    i_next, j_next = i+di[d], j+dj[d]

                    if is_ok(i_next, j_next, mat) and mat[i_next][j_next] == encode['.']:
                        mat[i_next][j_next] = -3
    
    mat = np.array(mat)
    return np.sum(mat%2 == 1)


def part2(inp: list[str]) -> int:
    return 0


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
