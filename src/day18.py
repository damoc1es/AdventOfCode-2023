DAY = 18


def area(points: list[tuple[int]]) -> int:
    perimeter = 0
    for i in range(len(points)-1):
        perimeter += abs(points[i+1][0]-points[i][0]) + abs(points[i+1][1]-points[i][1])

    # shoelace formula
    # A = 1/2 sum((y_i + y_(i+1))*(x_i-x_(i+1)))
    surface = 0
    for i in range(len(points)-1):
        surface += (points[i][1]+points[i+1][1])*(points[i][0]-points[i+1][0])
    surface = abs(surface)//2

    # pick's theorem
    # i = interior points
    # b = boundary points = perimeter
    # A = i + b/2 - 1 <=>
    # i = A - b/2 + 1
    interior = surface - perimeter // 2 + 1

    return interior + perimeter


def path_from_instructions(instr: list[tuple[str, int]]) -> list[tuple[int]]:
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    x = y = 0

    for direction, value in instr:
        if direction == 'L':
            y -= value
        elif direction == 'R':
            y += value
        elif direction == 'U':
            x -= value
        elif direction == 'D':
            x += value

        min_x, max_x = min(x, min_x), max(x, max_x)
        min_y, max_y = min(y, min_y), max(y, max_y)
    
    x, y = abs(min_x), abs(min_y)
    path = [(x, y)]

    for direction, value in instr:
        if direction == 'L':
            y -= value
        elif direction == 'R':
            y += value
        elif direction == 'U':
            x -= value
        elif direction == 'D':
            x += value
        path.append((x, y))
    return path


def part1(inp: list[str]) -> int:
    instr = []
    for line in inp:
        direction, value, _ = line.split()
        instr.append((direction, int(value)))

    return area(path_from_instructions(instr))


def part2(inp: list[str]) -> int:
    instr = []
    for line in inp:
        _, _, color = line.split()
        color = color[1:-1]

        if color[-1] == '0':
            direction = 'R'
        elif color[-1] == '1':
            direction = 'D'
        elif color[-1] == '2':
            direction = 'L'
        elif color[-1] == '3':
            direction = 'U'
        
        instr.append((direction, int(color[1:-1], 16)))

    return area(path_from_instructions(instr))


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
