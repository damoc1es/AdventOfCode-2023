from queue import Queue

DAY = 22


def get_bricks_and_cubes(inp: list[str]) -> tuple[dict, dict]:
    cubes = {}
    brick = {}

    shape_id = 0
    for line in inp:
        brick[shape_id] = []

        begin, end = line.split('~')
        x0, y0, z0 = [int(t) for t in begin.split(',')]
        x1, y1, z1 = [int(t) for t in end.split(',')]
        
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                for z in range(z0, z1+1):
                    cubes[(x, y, z)] = shape_id
                    brick[shape_id].append((x, y, z))
        
        shape_id += 1
    
    while True:
        is_sorted = True

        # for every brick, if it has an empty space below
        # every cube move it down
        for s_id, cs in brick.items():
            movable = True

            for (x, y, z) in cs:
                if ((x, y, z-1) in cubes.keys() and cubes[(x, y, z-1)] != s_id) or z == 1:
                    movable = False
                    break
            
            if movable:
                is_sorted = False
                for i in range(len(cs)):
                    x, y, z = cs[i]
                    brick[s_id][i] = (x, y, z-1)
                    cubes[(x, y, z-1)] = s_id
                    del cubes[(x, y, z)]
            
        if is_sorted:
            break
    
    return cubes, brick


def get_supports(brick: dict, cubes: dict) -> tuple[dict, dict]:
    supports = {k: set() for k in brick.keys()}
    is_supported = {k: set() for k in brick.keys()}

    for s_id, cs in brick.items():
        for (x, y, z) in cs:
            if (x, y, z+1) in cubes.keys() and cubes[(x, y, z+1)] != s_id:
                supports[s_id].add(cubes[(x, y, z+1)])
                is_supported[cubes[(x, y, z+1)]].add(s_id)
    
    return supports, is_supported


def get_disintegrable(supports: dict, is_supported: dict) -> set:
    disintegrable = set()

    for s_id in supports.keys():
        if len(supports[s_id]) == 0:
            disintegrable.add(s_id)
        else:
            ok = True
            for s_id2 in supports[s_id]:
                if len(is_supported[s_id2]) == 1:
                    ok = False
                    break
            if ok:
                disintegrable.add(s_id)
    
    return disintegrable


def part1(inp: list[str]) -> int:
    cubes, brick = get_bricks_and_cubes(inp)
    supports, is_supported = get_supports(brick, cubes)
    return len(get_disintegrable(supports, is_supported))


def part2(inp: list[str]) -> int:
    cubes, brick = get_bricks_and_cubes(inp)
    supports, is_supported = get_supports(brick, cubes)

    disintegrable = get_disintegrable(supports, is_supported)
    k = 0
    for s_id in brick.keys():
        if s_id in disintegrable:
            continue
        to_be_checked = set()

        _, is_supported2 = get_supports(brick, cubes)
        
        q = Queue()
        q.put(s_id)
        
        for s_id2 in supports[s_id]:
            q.put(s_id2)
            is_supported2[s_id2].remove(s_id)

        while not q.empty():
            s_id2 = q.get()
            to_be_checked.add(s_id2)

            if len(is_supported2[s_id2]) == 0:
                for s_id3 in supports[s_id2]:
                    q.put(s_id3)
                    if s_id2 in is_supported2[s_id3]:
                        is_supported2[s_id3].remove(s_id2)

        for s_id2 in to_be_checked:
            if len(is_supported2[s_id2]) == 0 and s_id2 != s_id:
                k += 1

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
