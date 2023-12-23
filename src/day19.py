from queue import Queue

DAY = 19


def result(rating: dict[str, int], wf: str, workflow: dict[str, list]) -> str:
    for condition in workflow[wf]:
        if len(condition) > 1:
            if condition[0][1] == '<':
                if rating[condition[0][0]] < condition[0][2]:
                    if condition[1] in ('R', 'A'):
                        return condition[1]
                    return result(rating, condition[1], workflow)
            elif rating[condition[0][0]] > condition[0][2]:
                if condition[1] in ('R', 'A'):
                    return condition[1]
                return result(rating, condition[1], workflow)
        else:
            if condition[0] in ('R', 'A'):
                return condition[0]
            return result(rating, condition[0], workflow)


def parse_input(inp: list[str]) -> tuple[dict, list]:
    workflows0 = []
    ratings0 = []
    ok = False
    for line in inp:
        if line == '':
            ok = True
            continue
        if not ok:
            workflows0.append(line)
        else: ratings0.append(line)
    
    workflow = {}
    for line in workflows0:
        label, rest = line.split('{')

        workflow[label] = []
        for condition in rest[:-1].split(','):
            if ':' not in condition:
                workflow[label].append((condition,))
            else:
                c, res = condition.split(':')
                c = (c[0], c[1], int(c[2:]))
                workflow[label].append((c, res))
    
    ratings = []
    for line in ratings0:
        x0, m0, a0, s0 = line.split(',')
        x = int(x0.split('=')[1])
        m = int(m0.split('=')[1])
        a = int(a0.split('=')[1])
        s = int(s0[:-1].split('=')[1])
        ratings.append({"x": x, "m": m, "a": a, "s": s})
    
    return workflow, ratings


def part1(inp: list[str]) -> int:
    workflow, ratings = parse_input(inp)
    
    S = 0
    for rating in ratings:
        if result(rating, "in", workflow) == 'A':
            S += sum(rating.values())
    return S


def part2(inp: list[str]) -> int:
    workflow, _ = parse_input(inp)
    
    S = 0
    q = Queue()

    q.put(("in", (1, 4000), (1, 4000), (1, 4000), (1, 4000)))

    while not q.empty():
        state, x, m, a, s = q.get()
        if state == 'R':
            continue
        if state == 'A':
            S += (x[1]-x[0]+1) * (m[1]-m[0]+1) * (a[1]-a[0]+1) * (s[1]-s[0]+1)
            continue

        for condition in workflow[state]:
            if len(condition) == 1:
                q.put((condition[0], x, m, a, s))
            else:
                if condition[0][1] == '<':
                    if condition[0][0] == 'x':
                        if x[0] <= condition[0][2] <= x[1]:
                            q.put((condition[1], (x[0], min(condition[0][2]-1, x[1])), m, a, s))
                            x = (max(x[0], condition[0][2]), x[1])
                        else: continue
                    elif condition[0][0] == 'm':
                        if m[0] <= condition[0][2] <= m[1]:
                            q.put((condition[1], x, (m[0], min(condition[0][2]-1, m[1])), a, s))
                            m = (max(m[0], condition[0][2]), m[1])
                        else: continue
                    elif condition[0][0] == 'a':
                        if a[0] <= condition[0][2] <= a[1]:
                            q.put((condition[1], x, m, (a[0], min(condition[0][2]-1, a[1])), s))
                            a = (max(a[0], condition[0][2]), a[1])
                        else: continue
                    else:
                        if s[0] <= condition[0][2] <= s[1]:
                            q.put((condition[1], x, m, a, (s[0], min(condition[0][2]-1, s[1]))))
                            s = (max(s[0], condition[0][2]), s[1])
                        else: continue
                else:
                    if condition[0][0] == 'x':
                        if x[0] <= condition[0][2] <= x[1]:
                            q.put((condition[1], (max(x[0], condition[0][2]+1), x[1]), m, a, s))
                            x = (x[0], min(x[1], condition[0][2]))
                        else: continue
                    elif condition[0][0] == 'm':
                        if m[0] <= condition[0][2] <= m[1]:
                            q.put((condition[1], x, (max(m[0], condition[0][2]+1), m[1]), a, s))
                            m = (m[0], min(m[1], condition[0][2]))
                        else: continue
                    elif condition[0][0] == 'a':
                        if a[0] <= condition[0][2] <= a[1]:
                            q.put((condition[1], x, m, (max(a[0], condition[0][2]+1), a[1]), s))
                            a = (a[0], min(a[1], condition[0][2]))
                        else: continue
                    else:
                        if s[0] <= condition[0][2] <= s[1]:
                            q.put((condition[1], x, m, a, (max(s[0], condition[0][2]+1), s[1])))
                            s = (s[0], min(s[1], condition[0][2]))
                        else: continue
    
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
