import networkx as nx

DAY = 25


def part1(inp: list[str]) -> int:
    graph = nx.Graph()
    # edges = []
    all_nodes = set()
    for line in inp:
        node0, nodes = line.split(': ')
        all_nodes.add(node0)
        for node in nodes.split():
            # edges.append((node0, node))
            graph.add_edge(node0, node, capacity=1)
            all_nodes.add(node)

    # for i in range(len(edges)):
    #     x0, y0 = edges[i]
    #     graph.remove_edge(x0, y0)
    #     for j in range(i+1, len(edges)):
    #         x1, y1 = edges[j]
    #         graph.remove_edge(x1, y1)
    #         for k in range(j+1, len(edges)):
    #             x2, y2 = edges[k]
    #             graph.remove_edge(x2, y2)
    #             if nx.number_connected_components(graph) == 2:
    #                 x, y = list(nx.connected_components(graph))
    #                 return len(x)*len(y)
    #             graph.add_edge(x2, y2)
    #         graph.add_edge(x1, y1)
    #     graph.add_edge(x0, y0)
    
    all_nodes = list(all_nodes)

    for i in range(len(all_nodes)):
        for j in range(i+1, len(all_nodes)):
            cuts, nodes = nx.minimum_cut(graph, all_nodes[i], all_nodes[j])
            if cuts == 3:
                return len(nodes[0])*len(nodes[1])
    
    return -1


def part2(inp: list[str]) -> int:
    return 42


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
