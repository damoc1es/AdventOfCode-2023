import z3

DAY = 24


def parse_input(inp: list[str]) -> tuple[list[tuple], list[tuple]]:
    position = []
    velocity = []

    for line in inp:
        pos, vel = line.split(' @ ')
        pos = tuple((int(x) for x in pos.split(', ')))
        vel = tuple((int(x) for x in vel.split(', ')))
        position.append(pos)
        velocity.append(vel)

    return position, velocity


def intersections_2d(position: list[tuple], velocity: list[tuple], hailstone_min: int, hailstone_max: int) -> int:
    k = 0
    for i in range(len(position)-1):
        for j in range(i+1, len(position)):
            a1, b1, _ = velocity[i]
            a2, b2, _ = velocity[j]
            x1, y1, _ = position[i]
            x2, y2, _ = position[j]

            d = (b1*a2-b2*a1)
            if d == 0:
                # print("parallel", i, j)
                continue

            t1 = (a2*(y2-y1) - b2*(x2-x1)) / d
            t2 = (a1*(y2-y1) - b1*(x2-x1)) / d
            if hailstone_min <= x1+t1*a1 <= hailstone_max and hailstone_min <= y1+t1*b1 <= hailstone_max and t1 > 0 and t2 > 0:
                # print("intersect", i, j)
                k += 1
    return k


def part1(inp: list[str]) -> int:
    positions, velocities = parse_input(inp)
    return intersections_2d(positions, velocities, 200000000000000, 400000000000000)


def part2(inp: list[str]) -> int:
    positions, velocities = parse_input(inp)

    px, py, pz, vx, vy, vz = z3.Ints("px py pz vx vy vz")

    solver = z3.Solver()
    for i in range(len(positions)):
        x0, y0, z0 = positions[i]
        a0, b0, c0 = velocities[i]

        # solver.add(px + vx * t == x0 + a0 * t) # => px - x0 == (a0 - vx) * t => (px - x0) / (a0 - vx) == t
        # solver.add(py + vy * t == y0 + b0 * t) # => py - y0 == (b0 - vy) * t => (py - y0) / (b0 - vy) == t
        # solver.add(pz + vz * t == z0 + c0 * t) # => pz - z0 == (c0 - vz) * t => (pz - z0) / (c0 - vz) == t
        # same t, so we have
        # (px - x0) / (a0 - vx) == (py - y0) / (b0 - vy)
        # (py - y0) / (b0 - vy) == (pz - z0) / (c0 - vz)
        # (py - y0) / (b0 - vy) == (px - x0) / (a0 - vx)
        # but if the first two are true the third has to be true, so we can get rid of it
        # changed for multiplication as it seems to make it faster 
        solver.add((px - x0) * (b0 - vy) == (py - y0) * (a0 - vx))
        solver.add((py - y0) * (c0 - vz) == (pz - z0) * (b0 - vy))
    
    solver.check()
    return solver.model().evaluate(px + py + pz).as_long()


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
