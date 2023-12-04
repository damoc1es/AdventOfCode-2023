DAY = 4


def part1(inp: list[str]) -> int:
    S = 0
    for line in inp:
        _, x = line.split(':')

        winning, owned = x.split(' | ')
        winning = [int(t) for t in winning.split()]
        owned = [int(t) for t in owned.split()]

        p = 0
        for o in owned:
            if o in winning:
                p += 1
        
        if p != 0:
            S += 2 ** (p-1)
            
    return S


def part2(inp: list[str]) -> int:
    cards = {t: 1 for t in range(1, len(inp)+1)}

    for line in inp:
        card, x = line.split(':')

        card = int(card.split()[1])

        winning, owned = x.split(' | ')
        winning = [int(t) for t in winning.split()]
        owned = [int(t) for t in owned.split()]

        score = 0
        for o in owned:
            if o in winning:
                score += 1
        
        if score != 0:
            for j in range(score):
                cards[j+card+1] += cards[card]
    
    return sum(cards.values())


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
