import numpy as np
from copy import deepcopy

DAY = 14

encode = {'#': 2, 'O': 1, '.': 0}
decode = {v: k for k, v in encode.items()}

NORTH, EAST, WEST, SOUTH = 1, 2, 3, 4


def pprint(lst: list[list[int]]) -> None:
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            print(decode[lst[i][j]], end=" ")
        print()
    print()


def move(mat: list[list[int]], direction: int) -> None:
    if direction in (NORTH, WEST):
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if mat[i][j] == encode['O']:
                    new_i, new_j = i, j

                    if direction == NORTH:
                        for k in range(i-1, -1, -1):
                            if mat[k][j] != encode['.']:
                                break
                            new_i = k
                    else: # WEST
                        for k in range(j-1, -1, -1):
                            if mat[i][k] != encode['.']:
                                break
                            new_j = k

                    mat[i][j] = encode['.']
                    mat[new_i][new_j] = encode['O']
    elif direction in (SOUTH, EAST):
        for i in range(len(mat)-1, -1, -1):
            for j in range(len(mat[i])-1, -1, -1):
                if mat[i][j] == encode['O']:
                    new_i, new_j = i, j

                    if direction == SOUTH:
                        for k in range(i+1, len(mat)):
                            if mat[k][j] != encode['.']:
                                break
                            new_i = k
                    else: # EAST
                        for k in range(j+1, len(mat[i])):
                            if mat[i][k] != encode['.']:
                                break
                            new_j = k

                    mat[i][j] = encode['.']
                    mat[new_i][new_j] = encode['O']


def calculate_load(mat: list[list[int]]) -> int:
    S = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == encode['O']:
                S += len(mat)-i
    return S


def part1(inp: list[str]) -> int:
    mat = [[encode[x] for x in line] for line in inp]
    move(mat, NORTH)
    return calculate_load(mat)


def part2(inp: list[str]) -> int:
    mat = [[encode[x] for x in line] for line in inp]

    cycles = 1000000000
    keep = 50

    olds = [-1 for _ in range(keep)]

    for i in range(cycles):
        move(mat, NORTH)
        move(mat, WEST)
        move(mat, SOUTH)
        move(mat, EAST)
        
        if mat in olds:
            olds = olds[olds.index(mat):]
            return calculate_load(olds[(cycles-i) % len(olds) - 1])
        olds = olds[1:]
        olds.append(deepcopy(mat))
    
    return calculate_load(mat)


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")
    
    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
