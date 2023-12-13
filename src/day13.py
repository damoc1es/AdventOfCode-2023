import numpy as np

DAY = 13


def part1(inp: list[str]) -> int:
    patterns = []
    mat = []
    for line in inp:
        if line == "":
            patterns.append(np.array(mat))
            mat = []
        else:
            mat.append([0 if x == '.' else 1 for x in line])
    patterns.append(np.array(mat))
    
    S = 0
    for pattern in patterns:
        rows, columns = np.shape(pattern)
        mirror = None
        for i in range(rows-1):
            if np.array_equal(pattern[i], pattern[i+1]):
                a, b = i, i+1
                ok = True
                while a >= 0 and b < rows:
                    if not np.array_equal(pattern[a], pattern[b]):
                        ok = False
                        break
                    a -= 1
                    b += 1
                if ok:
                    mirror = i+1
                    break
        
        vertical = False
        if not mirror:
            for i in range(columns-1):
                if np.array_equal(pattern[:, i], pattern[:, i+1]):
                    a, b = i, i+1
                    ok = True
                    while a >= 0 and b < columns:
                        if not np.array_equal(pattern[:, a], pattern[:, b]):
                            ok = False
                            break
                        a -= 1
                        b += 1
                    if ok:
                        mirror = i+1
                        vertical = True
                        break
        if mirror:
            if vertical:
                S += mirror
            else: S += mirror*100

    return S


def smudge_arr(arr1: np.array, arr2: np.array) -> int:
    return np.sum(arr1 != arr2)


def part2(inp: list[str]) -> int:
    patterns = []
    mat = []
    for line in inp:
        if line == "":
            patterns.append(np.array(mat))
            mat = []
        else:
            mat.append([0 if x == '.' else 1 for x in line])
    patterns.append(np.array(mat))
    
    S = 0
    for pattern in patterns:
        rows, columns = np.shape(pattern)
        mirror = None
        for i in range(rows-1):
            if smudge_arr(pattern[i], pattern[i+1]) <= 1:
                smudge = 0
                a, b = i, i+1
                while a >= 0 and b < rows:
                    smudge += smudge_arr(pattern[a], pattern[b])
                    a -= 1
                    b += 1
                if smudge == 1:
                    mirror = i+1
                    break
        
        vertical = False
        if not mirror:
            for i in range(columns-1):
                if smudge_arr(pattern[:, i], pattern[:, i+1]) <= 1:
                    smudge = 0
                    a, b = i, i+1
                    while a >= 0 and b < columns:
                        smudge += smudge_arr(pattern[:, a], pattern[:, b])
                        a -= 1
                        b += 1
                    if smudge == 1:
                        mirror = i+1
                        vertical = True
                        break
        if mirror:
            if vertical:
                S += mirror
            else: S += mirror*100

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
