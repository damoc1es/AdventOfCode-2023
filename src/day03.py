import numpy as np

DAY = 3

di = [0, 0, -1, 1, 1, -1, 1, -1]
dj = [1, -1, 0, 0, 1, -1, -1, 1]
digit = list("0123456789")


def part1(inp: list[str]) -> int:
    def neighbor(i, j, M) -> bool:
        for d in range(len(di)):
            i_next = i + di[d]
            j_next = j + dj[d]

            if M[i_next][j_next] is not None and M[i_next][j_next] not in digit:
                return True
        return False
    
    M = np.pad(inp, 1, constant_values=(None)).tolist()
    S = 0
    
    for i in range(1, len(M)-1):
        j = 1
        while j < len(M[i])-1:
            if M[i][j] in digit:
                nr = 0
                ok = neighbor(i, j, M)
                k = 0
                while M[i][j+k] in digit:
                    nr = nr * 10 + int(M[i][j+k])
                    ok = ok or neighbor(i, j+k, M)
                    k += 1
                if ok:
                    j += k
                    S += nr
            j += 1

    return S


def part2(inp: list[str]) -> int:
    def neighbor(i, j, M) -> tuple[int, int, str] | None:
        for d in range(len(di)):
            i_next = i + di[d]
            j_next = j + dj[d]

            if M[i_next][j_next] is not None and M[i_next][j_next] not in digit:
                return (i_next, j_next, M[i_next][j_next])
        return None
    
    M = np.pad(inp, 1, constant_values=(None)).tolist()
    M2 = np.zeros_like(M).tolist()

    S = 0
    
    for i in range(1, len(M)-1):
        j = 1
        while j < len(M[i])-1:
            if M[i][j] in digit:
                nr = 0
                ok = neighbor(i, j, M)
                k = 0
                while M[i][j+k] in digit:
                    nr = nr * 10 + int(M[i][j+k])
                    if not ok:
                        ok = neighbor(i, j+k, M)
                    k += 1
                if ok:
                    i2, j2, character = ok
                    if character == '*':
                        if M2[i2][j2] == 0:
                            M2[i2][j2] = (1, nr)
                        else:
                            M2[i2][j2] = (M2[i2][j2][0]+1, M2[i2][j2][1]*nr)
                    j += k
            j += 1
    
    for i in range(1, len(M2)-1):
        for j in range(1, len(M2[i])-1):
            if M2[i][j] != 0:
                if M2[i][j][0] == 2:
                    S += M2[i][j][1]
    return S


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [[None if x == '.' else x for x in line.strip()] for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
