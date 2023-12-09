DAY = 9


def reduce(L: list[int]) -> list[int]:
    L2 = []
    for i in range(len(L)-1):
        L2.append(L[i+1]-L[i])
    return L2


def part1(inp: list[list[int]]) -> int:
    S = 0
    for line in inp:
        last = []
        while set(line) != {0}:
            last.append(line[-1])
            line = reduce(line)
        
        S += sum(last)
    return S


def part2(inp: list[list[int]]) -> int:
    S = 0
    for line in inp:
        first = []
        while set(line) != {0}:
            first.append(line[0])
            line = reduce(line)
        
        current = 0
        for x in first[::-1]:
            current = x - current

        S += current
    return S


def read_input_file(filename: str) -> list[list[int]]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [[int(x) for x in line.split()] for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
