DAY = 6


def part1(inp: list[str]) -> int:
    ways = 1
    _, times = inp[0].split(':')
    _, distances = inp[1].split(':')
    times = [int(t) for t in times.split()]
    distances = [int(t) for t in distances.split()]


    for i in range(len(times)):
        time, distance = times[i], distances[i]
        ways0 = 0
        for j in range(time):
            left = time-j

            if left*j > distance:
                ways0 += 1
        ways *= ways0
    return ways


def part2(inp: list[str]) -> int:
    _, times = inp[0].split(':')
    _, distances = inp[1].split(':')
    
    time = int(''.join(times.split()))
    distance = int(''.join(distances.split()))

    ways = 0
    for j in range(time):
        left = time-j

        if left*j > distance:
            ways += 1
        
    return ways


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
