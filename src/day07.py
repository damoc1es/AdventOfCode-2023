from functools import cmp_to_key

DAY = 7

legend = {
    'five-of-a-kind': 1,
    'four-of-a-kind': 2,
    'full-house': 3,
    'three-of-a-kind': 4,
    'two-pair': 5,
    'one-pair': 6,
    'high-card': 7
}

strength = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}


def identify_hand(strengths: tuple[int]) -> str:
    d = {}
    for c in strengths:
        if c in d.keys():
            d[c] += 1
        else:
            d[c] = 1
    
    if 1 not in strengths:
        k = set(strengths)
        if len(k) == 1:
            return 'five-of-a-kind'
        if len(k) == 5:
            return 'high-card'
        if len(k) == 4:
            return 'one-pair'
        

        items = d.values()
        if 4 in items:
            return 'four-of-a-kind'
        if 2 in items and 3 in items:
            return 'full-house'
        if 3 in items:
            return 'three-of-a-kind'
        return 'two-pair'
    else:
        if len(d.keys()) == 1:
            return 'five-of-a-kind'
        R = None
        max_count = float('-inf')
        for x, y in d.items():
            if x != 1 and y > max_count:
                max_count = y

        for x, y in d.items():
            if y == max_count and x != 1:
                R = x
                break
        t2 = tuple(R if x == 1 else x for x in strengths)

        return identify_hand(t2)
    

def compare(hand1: tuple[str,int], hand2: tuple[str,int]) -> int:
    if legend[identify_hand(hand1[0])] > legend[identify_hand(hand2[0])]:
        return -1
    elif legend[identify_hand(hand1[0])] < legend[identify_hand(hand2[0])]:
        return 1
    else:
        if hand1[0] < hand2[0]:
            return -1
        if hand1[0] > hand1[0]:
            return 1
        return 0


def part1(inp: list[str]) -> int:
    hands = []
    for line in inp:
        strengths = tuple(strength[x] for x in line.split()[0])
        t = (strengths, int(line.split()[1]))
        hands.append(t)
    
    hands.sort(key=cmp_to_key(compare))
    
    winnings = 0
    for rank, hand in enumerate(hands):
        winnings += (rank+1)*hand[1]
    
    return winnings


def part2(inp: list[str]) -> int:
    strength['J'] = 1

    hands = []
    for line in inp:
        strengths = tuple(strength[x] for x in line.split()[0])
        t = (strengths, int(line.split()[1]))
        hands.append(t)
    
    hands.sort(key=cmp_to_key(compare))
    
    winnings = 0
    for rank, hand in enumerate(hands):
        winnings += (rank+1)*hand[1]
    
    strength['J'] = 11

    return winnings


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
