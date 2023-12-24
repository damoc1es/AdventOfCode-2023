import numpy as np
from queue import Queue

DAY = 21

encode = {'.': 0, '#': -2, 'S': 0}
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

            if is_ok(i_next, j_next, map) and map[i_next][j_next] == encode['.'] and map[i][j] < max_step+1:
                map[i_next][j_next] = map[i][j] + 1
                Q.put((i_next, j_next))


def solve(mat: list[list], step: int) -> int:
    start = (len(mat)//2, len(mat)//2)
    
    Lee(mat, start, step)
    
    mat = np.array(mat)
    return np.sum(((mat%2 != step%2) & (mat > 0)))


def get_mat_of_scale(inp: list[str], scale: int) -> list[list]:
    mat = []
    for line in inp:
        mat.append([encode[x] for x in line])
    
    mat = np.tile(np.array(mat), (2*scale-1, 2*scale-1)).tolist()
    mat[len(mat)//2][len(mat)//2] = 1
    return mat


def part1(inp: list[str]) -> int:
    return solve(get_mat_of_scale(inp, 1), 64)


def part2(inp: list[str]) -> int:
    step = 26501365
    n = len(inp)

    xs = [n//2 + i*n for i in range(3)]
    ys = [solve(get_mat_of_scale(inp, i+1), x) for i, x in enumerate(xs)]
    
    # a*0^2 + b*0 + c = y0 => c = y0
    # a*1^2 + b*1 + c = y1 => a + b + c = y1 => a + b = y1 - c
    # a*2^2 + b*2 + c = y2 => 4a + 2b + c = y2 => 4a + 2b = y2 - c

    # a + b = y1 - c
    # 4a + 2b = y2 - c

    # b = y1 - c - a
    # 4a + 2(y1 - c - a) = y2 - c
    # 4a + 2y1 - 2c - 2a = y2 - c
    # 2a = y2 - c - 2y1 + 2c
    # 2a = y2 + c - 2y1
    # a = (y2 + c - 2y1) / 2
    
    c = int(ys[0])
    a = int((ys[2] + c - 2*ys[1]) // 2)
    b = int(ys[1] - c - a)

    # step = n//2 + i * n
    i = (step-n//2) // n
    
    return (a * (i**2)) + (b * i) + c


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
