from math import lcm

DAY = 20

HIGH_PULSE, LOW_PULSE = 1, 2
FLIP_FLOP, CONJUNCTION, BROADCAST = 1, 2, 3

decode = {HIGH_PULSE: "-high-", LOW_PULSE: "-low-"}


class Graph:
    low_pulses = 0
    high_pulses = 0
    STOP = False
    stopping_labels = {}
    k = 0


    class Node:
        def __init__(self, label: str, comp: int | None, part):
            self.label = label
            self.component = comp
            self.inputs = []
            self.outputs = []
            self.part = part

            self.on = False # FlipFlop
            self.remembers = {} # Conjunction


        def receive(self, sender_node: str, pulse: int):
            # print(f"{sender_node} {decode[pulse]}> {self.label}")

            if pulse == LOW_PULSE:
                Graph.low_pulses += 1
            elif pulse == HIGH_PULSE: Graph.high_pulses += 1
            
            if self.component == FLIP_FLOP:
                if pulse == HIGH_PULSE:
                    return
                elif pulse == LOW_PULSE:
                    if self.on:
                        self.on = False
                        self.send(LOW_PULSE)
                    else:
                        self.on = True
                        self.send(HIGH_PULSE)
            elif self.component == CONJUNCTION:
                self.remembers[sender_node] = pulse
                if LOW_PULSE not in self.remembers.values():
                    self.send(LOW_PULSE)
                else:
                    self.send(HIGH_PULSE)
            elif self.component == BROADCAST:
                self.send(pulse)
        

        def send(self, pulse: int):
            if self.part == 2 and self.label in Graph.stopping_labels.keys() and pulse == HIGH_PULSE:
                Graph.stopping_labels[self.label] = Graph.k
                # print(Graph.k, Graph.stopping_labels)
                if None not in Graph.stopping_labels.values():
                    Graph.STOP = True

            for node in self.outputs:
                node.receive(self.label, pulse)


        def add_input(self, node):
            self.inputs.append(node)
            if self.component == CONJUNCTION:
                self.remembers[node.label] = LOW_PULSE


        def add_output(self, node):
            self.outputs.append(node)
        

        def __str__(self):
            return f"{self.label}: {self.component} | {len(self.inputs)} | {len(self.outputs)} | {self.on} | {len(self.remembers)}"


    def __init__(self, components: dict[str, Node]):
        self.component = components
        Graph.low_pulses = 0
        Graph.high_pulses = 0
        Graph.STOP = False
        Graph.stopping_labels = {}
        Graph.k = 0


    def push_button(self):
        Graph.k += 1
        self.component['broadcaster'].receive("button", LOW_PULSE)


    def from_input(inp: list[str], part: int):
        comps = {}
        for line in inp:
            t, _ = line.split(' -> ')
            if t[0] == '%':
                comps[t[1:]] = Graph.Node(t[1:], FLIP_FLOP, part)
            elif t[0] == '&':
                comps[t[1:]] = Graph.Node(t[1:], CONJUNCTION, part)
            elif t == 'broadcaster':
                comps[t] = Graph.Node(t, BROADCAST, part)
            else:
                comps[t] = Graph.Node(t, None, part)

        for line in inp:
            x, t = line.split(' -> ')
            if x[0] in ('%', '&'):
                x = x[1:]
            for label in t.split(', '):
                if label not in comps.keys():
                    comps[label] = Graph.Node(label, None, part)
                
                comps[x].add_output(comps[label])
                comps[label].add_input(comps[x])
        return Graph(comps)


def part1(inp: list[str]) -> int:
    g = Graph.from_input(inp, 1)

    for _ in range(1000):
        g.push_button()
    
    return Graph.low_pulses * Graph.high_pulses


def part2(inp: list[str]) -> int:
    node = Graph.from_input(inp, 1).component["rx"].inputs[0]

    g = Graph.from_input(inp, 2)
    Graph.stopping_labels = {k.label: None for k in node.inputs}
    while Graph.STOP != True:
        g.push_button()
    
    return lcm(*Graph.stopping_labels.values())


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
