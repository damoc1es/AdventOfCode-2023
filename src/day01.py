DAY = 1


def part1(inp: list[str]) -> int:
    S = 0
    for line in inp:
        x = y = None
        for c in line:
            if c in "123456789":
                if x is None:
                    x = int(c)
                y = int(c)

        S += x*10+y
    
    return S


def part2(inp: list[str]) -> int:
    S = 0
    for line in inp:
        digits = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
        x = y = 0
        place_x = place_y = None

        for k, v in digits.items():
            digit0, digit1 = line.find(k), line.rfind(k)
            string0, string1 = line.find(v), line.rfind(v)
            value = int(k)

            if digit0 != -1:
                if place_x is None or digit0 < place_x:
                    place_x, x = digit0, value

                if place_y is None or digit1 > place_y:
                    place_y, y = digit1, value
            
            if string0 != -1:
                if place_x is None or string0 < place_x:
                    place_x, x = string0, value

                if place_y is None or string1 > place_y:
                    place_y, y = string1, value

        S += x*10+y
    
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
