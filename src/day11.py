import numpy as np

DAY = 11


def manhattan(p1: tuple[int], p2: tuple[int]) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def part1(inp: list[list[int]]) -> int:
    columns = ~np.array(inp).any(axis=0)
    rows = ~np.array(inp).any(axis=1)

    nodes = []
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            if inp[i][j] == 1:
                z1 = int(rows[:i].sum())
                z2 = int(columns[:j].sum())
                nodes.append((i+z1, j+z2))

    S = 0
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i != j:
                S += manhattan(nodes[i], nodes[j])
    
    return S


def part2(inp: list[list[int]]) -> int:
    columns = ~np.array(inp).any(axis=0)
    rows = ~np.array(inp).any(axis=1)

    factor = 1000000-1

    nodes = []
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            if inp[i][j] == 1:
                z1 = int(rows[:i].sum())
                z2 = int(columns[:j].sum())
                nodes.append((i+factor*z1, j+factor*z2))

    S = 0
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if i != j:
                S += manhattan(nodes[i], nodes[j])
    
    return S


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [[1 if x == '#' else 0 for x in line.strip()] for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
