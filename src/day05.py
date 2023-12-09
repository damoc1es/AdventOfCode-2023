DAY = 5


def convertor(val: int, map: dict[int,tuple[int,int]]):
    for val0, t in map.items():
        exp0, range0 = t
        if val0 <= val < val0+range0:
            return val + exp0-val0
    return val


def part1(inp: list[str]) -> int:
    maps = {}
    current = ""
    seeds = []

    for line in inp:
        if line.find("seeds: ") != -1:
            seeds = [int(t) for t in line.split(": ")[1].split()]
        elif line == "":
            continue
        elif line.split()[1] == "map:":
            current = line.split()[0]
            maps[current] = {}
        else:
            x, y, r = [int(t) for t in line.split()]
            maps[current][y] = (x, r)
    
    locations = []
    for seed in seeds:
        soil = convertor(seed, maps['seed-to-soil'])
        fertilizer = convertor(soil, maps['soil-to-fertilizer'])
        water = convertor(fertilizer, maps['fertilizer-to-water'])
        light = convertor(water, maps['water-to-light'])
        temperature = convertor(light, maps['light-to-temperature'])
        humidity = convertor(temperature, maps['temperature-to-humidity'])
        location = convertor(humidity, maps['humidity-to-location'])
        locations.append(location)
    return min(locations)


def part2(inp: list[str]) -> int:
    maps = {}
    current = ""
    seed_pair = []
    seeds = []

    for line in inp:
        if line.find("seeds: ") != -1:
            seeds = [int(t) for t in line.split(": ")[1].split()]
            for i in range(0, len(seeds), 2):
                seed_pair.append((seeds[i], seeds[i+1]))
        elif line == "":
            continue
        elif line.split()[1] == "map:":
            current = line.split()[0]
            maps[current] = {}
        else:
            x, y, r = [int(t) for t in line.split()]
            maps[current][y] = (x, r)
    
    min_loc = float('inf')
    for s, r in seed_pair:
        print(s, r)
        for seed in range(s, s+r):
            soil = convertor(seed, maps['seed-to-soil'])
            fertilizer = convertor(soil, maps['soil-to-fertilizer'])
            water = convertor(fertilizer, maps['fertilizer-to-water'])
            light = convertor(water, maps['water-to-light'])
            temperature = convertor(light, maps['light-to-temperature'])
            humidity = convertor(temperature, maps['temperature-to-humidity'])
            location = convertor(humidity, maps['humidity-to-location'])
            min_loc = min(location, min_loc)
    
    return min_loc


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
