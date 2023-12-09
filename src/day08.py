from itertools import cycle
from math import lcm

DAY = 8


class Node:
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left}, {self.right})"


def part1(inp: list[str]) -> int:
    steps = list(inp[0])
    map = {}
    for i in range(2, len(inp)):
        a, b = inp[i].split(' = (')
        b, c = b.split(', ')
        c = c[:-1]
        map[a] = Node(b, c)

    k = 0
    current = 'AAA'
    for step in cycle(steps):
        k += 1
        if step == 'L':
            current = map[current].left
        else:
            current = map[current].right

        if current == 'ZZZ':
            break

    return k


def part2(inp: list[str]) -> int:
    steps = list(inp[0])
    map = {}
    ending = {}
    for i in range(2, len(inp)):
        a, b = inp[i].split(' = (')
        b, c = b.split(', ')
        c = c[:-1]
        map[a] = Node(b, c)

    k = 0
    currents = []
    for key in map.keys():
        if key[2] == 'A':
            currents.append((key, key))
            ending[key] = None
    
    for step in cycle(steps):
        k += 1
        if step == 'L':
            for i in range(len(currents)):
                currents[i] = (map[currents[i][0]].left, currents[i][1])
        else:
            for i in range(len(currents)):
                currents[i] = (map[currents[i][0]].right, currents[i][1]) 

        for c in currents:
            if c[0][2] == 'Z':
                ending[c[1]] = k
        
        for i in range(len(currents)-1, 0, -1):
            if currents[i][0][2] == 'Z':
                currents.pop(i)

        if None not in ending.values():
            return lcm(*ending.values())

    return k


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
