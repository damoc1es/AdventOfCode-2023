from functools import cache
import re

DAY = 12


@cache
def arrangements(row: str, group: tuple[int]) -> int:
    if len(group) == 0: # no groups left
        if '#' in row: # bad (it would've been another group)
            return 0
        return 1 # the ending of a good arrangement ("."s or "?"s that transform in ".")
    
    if sum(group) > len(row): # no arrangement this way
        return 0
    
    # get rid of "."
    if row[0] == '.':
        return arrangements(row[1:], group)
    
    S = 0

    if row[0] == '?': # the case where "?" turns into a "."
        S += arrangements(row[1:], group)
    
    if '.' not in row[:group[0]]: # is possible to make a group
        # final group / continuation of group is "." or "?" (valid)
        if (len(row) <= group[0] or row[group[0]] != '#'):
            S += arrangements(row[(group[0]+1):], group[1:])
    return S


def simplify(row: str, groups: tuple[int]) -> (str, tuple[int]):
    row = re.sub(r"\.+", ".", row)
    
    broken, begin = False, 0
    for i in range(len(row)):
        match row[i]:
            case '?':
                break
            case '#':
                broken = True
            case _:
                if broken:
                    groups = groups[1:]
                    broken = False
                    begin = i

    broken, end = False, len(row)
    for i in range(len(row)-1, 0, -1):
        match row[i]:
            case '?':
                break
            case '#':
                broken = True
            case _:
                if broken:
                    groups = groups[:-1]
                    broken = False
                    end = i

    return row[begin:end], groups


def part1(inp: list[str]) -> int:
    S = 0
    for line in inp:
        row, groups = line.split()
        groups = tuple(int(x) for x in groups.split(','))

        S += arrangements(*simplify(row, groups))
    return S


def part2(inp: list[str]) -> int:
    S = 0
    for line in inp:
        row, groups = line.split()
        groups = tuple(int(x) for x in groups.split(','))

        row = "?".join((row, row, row, row, row))
        groups = groups + groups + groups + groups + groups

        S += arrangements(*simplify(row, groups))
    return S


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
