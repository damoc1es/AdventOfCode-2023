# May this code never be touched up again.

import numpy as np
from queue import Queue
import networkx as nx

DAY = 23

encode = {
    '#': '#', '.': ' ',
    '>': 'E', '<': 'W',
    '^': 'N', 'v': 'S'
}

di = (0, 0, -1, 1)
dj = (1, -1, 0, 0)


class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.edges = []
    
    def add(self, other: tuple[int], value: int) -> None:
        self.edges.append((other, value))
    
    def update(self, other: tuple[int], new_value: int) -> None:
        for i in range(len(self.edges)):
            if self.edges[i][0] == other:
                self.edges[i] = (other, new_value)
                break
    
    def remove(self, other: tuple[int]) -> None:
        for i in range(len(self.edges)):
            if self.edges[i][0] == other:
                self.edges.remove(self.edges[i])
                break
    
    def find(self, other: tuple[int]) -> int | None:
        for i in range(len(self.edges)):
            if self.edges[i][0] == other:
                return self.edges[i][1]
        return None
    
    def __str__(self):
        return f"Node({self.x}, {self.y}), {len(self.edges)} edges"


class Graph:
    def __init__(self, nodes: dict[tuple, Node], start: tuple[int], end: tuple[int]):
        self.nodes = nodes
        self.start = start
        self.end = end
    
    def to_nx(self) -> nx.Graph:
        G = nx.DiGraph()
        
        for node, adj in self.nodes.items():
            for other, value in adj.edges:
                G.add_edge(node, other, weight=value)
        return G
    
    def nodes_attached(self, coord: tuple[int]) -> int:
        k = 0
        for node in self.nodes.values():
            if node.x != coord[0] or node.y != coord[1]:
                if node.find(coord):
                    k += 1
        return k

    def simplify(self) -> None:
        ok = True
        while ok:
            ok = False
            for coord, node in self.nodes.items():
                if len(node.edges) == 2 and self.nodes_attached(coord) == 2:
                    p1, p2 = node.edges
                    x = self.nodes[p1[0]].find(coord)
                    y = self.nodes[p2[0]].find(coord)
                    if x and y:
                        ok = True
                        self.nodes[p1[0]].add(p2[0], p2[1] + x)
                        self.nodes[p2[0]].add(p1[0], p1[1] + y)
                        self.nodes[p1[0]].remove(coord)
                        self.nodes[p2[0]].remove(coord)
                        self.nodes.pop(coord)
                        break


def print_matrix(M: list[list], path: list[tuple[int]]) -> None:
    for i in range(len(M)):
        for j in range(len(M[i])):
            if (i, j) in path:
                print('X', end='')
            else: print(M[i][j], end='')
        print()


def graph_nodes_are_intersections(inp: list[str]) -> Graph:
    M = [[encode[c] for c in line] for line in inp]
    M = np.pad(M, 1, constant_values=('#')).tolist()

    START = (1, 2)
    END = (len(M)-2, len(M[0])-3)

    GRAPH = {}
    for i in range(1, len(M)-1):
        for j in range(1, len(M[i])-1):
            if M[i][j] != '#':
                k1 = k2 = 0

                if M[i-1][j] != '#': k1 += 1
                if M[i+1][j] != '#': k1 += 1
                if M[i][j-1] != '#': k2 += 1
                if M[i][j+1] != '#': k2 += 1

                if k1 and k2:
                    GRAPH[(i, j)] = Node(i, j)

    GRAPH[START] = Node(*START)
    GRAPH[END] = Node(*END)

    for i in range(1, len(M)-1):
        for j in range(1, len(M[i])-1):
            if (i, j) in GRAPH:
                if M[i][j] != '#':
                    d = 0
                    for k in range(i-1, 0, -1):
                        d += 1
                        if M[k][j] == '#':
                            break
                        if (k, j) in GRAPH:
                            GRAPH[(i, j)].add((k, j), d)
                            break
                
                    d = 0
                    for k in range(i+1, len(M)):
                        d += 1
                        if M[k][j] == '#':
                            break
                        if (k, j) in GRAPH:
                            GRAPH[(i, j)].add((k, j), d)
                            break
                    
                    d = 0
                    for k in range(j-1, 0, -1):
                        d += 1
                        if M[i][k] == '#':
                            break
                        if (i, k) in GRAPH:
                            GRAPH[(i, j)].add((i, k), d)
                            break
                
                    d = 0
                    for k in range(j+1, len(M[i])):
                        d += 1
                        if M[i][k] == '#':
                            break
                        if (i, k) in GRAPH:
                            GRAPH[(i, j)].add((i, k), d)
                            break
    
    return Graph(GRAPH, START, END)


def graph_nodes_are_slopes(inp: list[str]) -> Graph:
    M = [[encode[c] for c in line] for line in inp]
    M = np.pad(M, 1, constant_values=('#')).tolist()
    CHECKED = np.full_like(M, -1).tolist()

    START = (1, 2)
    END = (len(M)-2, len(M[0])-3)

    GRAPH = {}
    GRAPH[START] = Node(*START)
    GRAPH[END] = Node(*END)

    CHECKED[START[0]][START[1]] = 1

    Q = Queue()
    # putting the next cell and the most recent node
    Q.put(((START[0]+1, START[1]), START))

    direction = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}

    put = set()

    while not Q.empty():
        current, prev_node = Q.get()
        i, j = current

        for d in range(4):
            i_next = i + di[d]
            j_next = j + dj[d]

            if M[i][j] in direction and (i-i_next, j-j_next) == direction[M[i][j]]:
                continue

            if (M[i_next][j_next] in direction and (i_next-i, j_next-j) == direction[M[i_next][j_next]]):
                CHECKED[i_next][j_next] = 1
                if (i_next, j_next) not in GRAPH:
                    GRAPH[(i_next, j_next)] = Node(i_next, j_next)
                GRAPH[prev_node].add((i_next, j_next), 0)

                if ((i_next, j_next), (i_next, j_next)) not in put:
                    Q.put(((i_next, j_next), (i_next, j_next)))
                    put.add(((i_next, j_next), (i_next, j_next)))
            
            elif (i_next, j_next) == END:
                CHECKED[i_next][j_next] = 1
                GRAPH[prev_node].add((i_next, j_next), 0)
            
            elif M[i_next][j_next] == ' ':
                CHECKED[i_next][j_next] = 1
                if ((i_next, j_next), prev_node) not in put:
                    Q.put(((i_next, j_next), prev_node))
                    put.add(((i_next, j_next), prev_node))
    
    return Graph(GRAPH, START, END)


def lee(inp: list[list], start: tuple[int], end: tuple[int]) -> int:
    mat = [[encode[c] for c in line] for line in inp]
    mat = np.pad(mat, 1, constant_values=('#')).tolist()
    dist = np.full_like(mat, -1, dtype=int).tolist()

    Q = Queue()
    Q.put(start)
    dist[start[0]][start[1]] = 0

    direction = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}

    while not Q.empty():
        i, j = Q.get()

        if mat[i][j] in direction:
            i_next, j_next = i + direction[mat[i][j]][0], j + direction[mat[i][j]][1]
            if dist[i_next][j_next] == -1 and mat[i_next][j_next] != '#':
                dist[i_next][j_next] = dist[i][j] + 1
                Q.put((i_next, j_next))
            continue

        for d in range(4):
            i_next = i + di[d]
            j_next = j + dj[d]

            if (i_next, j_next) == end:
                return dist[i][j] + 1
            if dist[i_next][j_next] == -1 and mat[i_next][j_next] != '#':
                dist[i_next][j_next] = dist[i][j] + 1
                Q.put((i_next, j_next))
    
    return -1


def update_distances(inp: list[str], graph: Graph) -> None:
    for node in graph.nodes.values():
        p1 = node.x, node.y
        for p2, _ in node.edges:
            graph.nodes[p1].update(p2, lee(inp, p1, p2))


def DFS(graph: Graph, node: tuple[int], visited: list[tuple[int]]) -> int:
    if node == graph.end:
        return 0 #, visited.copy()

    max_value = float("-inf")
    # max_visited = set()
    visited.append(node)

    for other, value in graph.nodes[node].edges:
        if other not in visited:
            value2 = DFS(graph, other, visited) #
            if value + value2 > max_value:
                max_value = value + value2
                # max_visited = visited2

    visited.pop()
    return max_value # , max_visited


def part1(inp: list[str]) -> int:
    graph = graph_nodes_are_slopes(inp)
    update_distances(inp, graph)
    val = DFS(graph, graph.start, [])
    return val


def part2(inp: list[str]) -> int:
    graph = graph_nodes_are_intersections(inp)
    graph.simplify()
    xgraph = graph.to_nx()

    max_weight = float("-inf")
    for path in nx.all_simple_paths(xgraph, graph.start, graph.end):
        weight = 0
        for i in range(len(path)-1):
            weight += xgraph[path[i]][path[i+1]]['weight']
        if weight > max_weight:
            max_weight = weight

    return max_weight


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    # input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
