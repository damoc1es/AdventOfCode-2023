import numpy as np
from queue import Queue

DAY = 10

NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

d = {
    '|': (NORTH, SOUTH),
    '-': (WEST, EAST),
    'L': (NORTH, EAST),
    'J': (NORTH, WEST),
    '7': (WEST, SOUTH),
    'F': (SOUTH, EAST),
    '.': (),
}


def Lee(map: list[list], map0: list[list], start: tuple[int]) -> None:
    Q = Queue()
    Q.put(start)
    map0[start[0]][start[1]] = 0

    while not Q.empty():
        i, j = Q.get()
        
        for di, dj in d[map[i][j]]:
            i_next, j_next = i+di, j+dj
            if map[i_next][j_next] != '.' and map0[i_next][j_next] == -1:
                map0[i_next][j_next] = map0[i][j] + 1
                Q.put((i_next, j_next))


def part1(inp: list[str]) -> int:
    map = [list(row) for row in inp]
    map = np.pad(map, 1, constant_values='.')
    map0 = np.full_like(map, -1, dtype=np.int32).tolist()
    map = map.tolist()

    START = None
    for i, row in enumerate(map):
        for j, x in enumerate(row):
            if x == 'S':
                START = (i, j)
                break
        if START:
            break
    
    d['S'] = []
    if SOUTH in d[map[START[0]+NORTH[0]][START[1]+NORTH[1]]]:
        d['S'].append(NORTH)
    if NORTH in d[map[START[0]+SOUTH[0]][START[1]+SOUTH[1]]]:
        d['S'].append(SOUTH)
    if WEST in d[map[START[0]+EAST[0]][START[1]+EAST[1]]]:
        d['S'].append(EAST)
    if EAST in d[map[START[0]+WEST[0]][START[1]+WEST[1]]]:
        d['S'].append(WEST)
    
    Lee(map, map0, START)

    return np.max(map0)


def fill_seq(map0: list[list]) -> None:
    q = Queue()

    i, j = 0, 0
    q.put((i, j))
    map0[i][j] = -2

    di0 = [0, 0, 1, -1]
    dj0 = [1, -1, 0, 0]

    while not q.empty():
        i, j = q.get()
        for d in range(4):
            i_next = i+di0[d]
            j_next = j+dj0[d]
            if i_next >= 0 and j_next >= 0 and i_next < len(map0) and j_next < len(map0[0]) and map0[i_next][j_next] == -1:
                map0[i_next][j_next] = -2
                q.put((i_next, j_next))


def insert_between(arr: np.array, fill_value) -> np.array:
    out = np.full(2*np.array(arr.shape)-1, dtype=arr.dtype, fill_value=fill_value)
    out[::2,::2] = arr
    return out


def part2(inp: list[str]) -> int:
    map = [list(row) for row in inp]
    map = np.pad(map, 1, constant_values='.')
    map0 = np.full_like(map, -1, dtype=np.int32).tolist()
    map = map.tolist()

    START = None
    for i, row in enumerate(map):
        for j, x in enumerate(row):
            if x == 'S':
                START = (i, j)
                break
        if START:
            break
    
    d['S'] = []
    if SOUTH in d[map[START[0]+NORTH[0]][START[1]+NORTH[1]]]:
        d['S'].append(NORTH)
    if NORTH in d[map[START[0]+SOUTH[0]][START[1]+SOUTH[1]]]:
        d['S'].append(SOUTH)
    if WEST in d[map[START[0]+EAST[0]][START[1]+EAST[1]]]:
        d['S'].append(EAST)
    if EAST in d[map[START[0]+WEST[0]][START[1]+WEST[1]]]:
        d['S'].append(WEST)
    
    Lee(map, map0, START)
    
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map0[i][j] == -1:
                map[i][j] = '.'

    map0 = insert_between(np.array(map0), -1).tolist()
    map = insert_between(np.array(map), '.').tolist()
    
    for i in range(len(map)):
        for j in range(1, len(map[i]), 2):
            if EAST in d[map[i][j-1]] and WEST in d[map[i][j+1]]:
                map[i][j] = '-'
                map0[i][j] = 0

    for i in range(1, len(map), 2):
        for j in range(len(map[i])):
            if SOUTH in d[map[i-1][j]] and NORTH in d[map[i+1][j]]:
                map[i][j] = '|'
                map0[i][j] = 0

    fill_seq(map0)

    map0 = np.array(map0)
    map0 = np.delete(map0, list(range(1, map0.shape[0], 2)), axis=0)
    map0 = np.delete(map0, list(range(1, map0.shape[1], 2)), axis=1)
    
    unique, counts = np.unique(map0, return_counts=True)
    return dict(zip(unique, counts))[-1]


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
