import re

DAY = 15


def HASH(string: str) -> int:
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(inp: list[str]) -> int:
    S = 0
    for string in inp:
        S += HASH(string)
    return S


def part2(inp: list[str]) -> int:
    Map = [[] for _ in range(256)]

    for string in inp:
        label, nr = re.split(r'[-=]', string)
        hash_label = HASH(label)
        
        found = False
        for i in range(len(Map[hash_label])):
            if Map[hash_label][i][0] == label:
                if nr == '':
                    Map[hash_label].remove(Map[hash_label][i])
                else:
                    Map[hash_label][i] = (label, int(nr))
                found = True
                break
        
        if not found and nr != '':
            Map[hash_label].append((label, int(nr)))

    focusing_power = 0

    for i in range(len(Map)):
        for j in range(len(Map[i])):
            focusing_power += ((i+1) * (j+1) * Map[i][j][1])
    
    return focusing_power


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return inp[0].split(',')


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
