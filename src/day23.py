import numpy as np
from queue import PriorityQueue, Queue

DAY = 23

encode = {
    '#': '#', '.': ' ',
    '>': 'E', '<': 'W',
    '^': 'N', 'v': 'S'
}


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []
    
    def add(self, other, value):
        self.edges.append((other, value))
    
    def __str__(self):
        return f"Node({self.x}, {self.y}), {len(self.edges)} edges"


class Graph:
    def __init__(self, nodes, start, end):
        self.nodes = nodes
        self.start = start
        self.end = end


def print_matrix(M: list[list], path):
    for i in range(len(M)):
        for j in range(len(M[i])):
            if (i, j) in path:
                print('X', end='')
            # elif type(M[i][j]) == int:
            #     print(M[i][j] % 10, end='')
            else: print(M[i][j], end='')
        print()


def generate_graph(inp: list[str]) -> Graph:
    M = []
    for line in inp:
        M.append([encode[c] for c in line])
    M = np.pad(M, 1, constant_values=('#')).tolist()
    START = (1, 2)
    END = (len(M)-2, len(M[0])-3)

    GRAPH = {}
    for i in range(1, len(M)-1):
        for j in range(1, len(M[i])-1):
            if M[i][j] == ' ':
                k1 = k2 = 0

                if M[i-1][j] != '#': k1 += 1
                if M[i+1][j] != '#': k1 += 1
                if M[i][j-1] != '#': k2 += 1
                if M[i][j+1] != '#': k2 += 1

                if k1 and k2:
                    GRAPH[(i, j)] = Node(i, j)
            elif M[i][j] != '#':
                GRAPH[(i, j)] = Node(i, j)

    GRAPH[START] = Node(*START)
    GRAPH[END] = Node(*END)

    for i in range(1, len(M)-1):
        for j in range(1, len(M[i])-1):
            if (i, j) in GRAPH:
                # go up until wall
                d = 0
                if M[i][j] == ' ' or M[i][j] == 'N':
                    for k in range(i-1, 0, -1):
                        d += 1
                        if M[k][j] == '#':
                            break
                        if (k, j) in GRAPH:
                            GRAPH[(i, j)].add((k, j), d)
                
                # go down until wall
                d = 0
                if M[i][j] == ' ' or M[i][j] == 'S':
                    for k in range(i+1, len(M)):
                        d += 1
                        if M[k][j] == '#':
                            break
                        if (k, j) in GRAPH:
                            GRAPH[(i, j)].add((k, j), d)
                
                # go left until wall
                d = 0
                if M[i][j] == ' ' or M[i][j] == 'W':
                    for k in range(j-1, 0, -1):
                        d += 1
                        if M[i][k] == '#':
                            break
                        if (i, k) in GRAPH:
                            GRAPH[(i, j)].add((i, k), d)
                
                # go right until wall
                d = 0
                if M[i][j] == ' ' or M[i][j] == 'E':
                    for k in range(j+1, len(M[i])):
                        d += 1
                        if M[i][k] == '#':
                            break
                        if (i, k) in GRAPH:
                            GRAPH[(i, j)].add((i, k), d)
    # print_matrix(M, GRAPH)
    return Graph(GRAPH, START, END)


def generate_graph_2(inp: list[str]) -> Graph:
    M = [[encode[c] for c in line] for line in inp]
    M = np.pad(M, 1, constant_values=('#')).tolist()

    DIST = np.full_like(M, -1).tolist()
    START = (1, 2)
    END = (len(M)-2, len(M[0])-3)

    GRAPH = {}
    GRAPH[START] = Node(*START)
    GRAPH[END] = Node(*END)

    DIST[START[0]][START[1]] = 0
    DIST[START[0]+1][START[1]] = 1

    di = [0, 0, -1, 1]
    dj = [1, -1, 0, 0]

    Q = Queue()
    # putting the next cell and the most recent node
    Q.put(((START[0]+1, START[1]), START))

    direction = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}

    put = set()

    while not Q.empty():
        current, prev_node = Q.get()
        i, j = current
        prev_i, prev_j = prev_node

        for d in range(4):
            i_next = i + di[d]
            j_next = j + dj[d]


            if (M[i_next][j_next] in direction and (i_next-i, j_next-j) == direction[M[i_next][j_next]]):
                DIST[i_next][j_next] = DIST[i][j] + 1
                if (i_next, j_next) not in GRAPH:
                    GRAPH[(i_next, j_next)] = Node(i_next, j_next)
                GRAPH[prev_node].add((i_next, j_next), (DIST[i_next][j_next]-DIST[prev_i][prev_j]))
                if ((i_next, j_next), (i_next, j_next)) not in put:
                    Q.put(((i_next, j_next), (i_next, j_next)))
                    put.add(((i_next, j_next), (i_next, j_next)))
            
            elif (i_next, j_next) == END:
                DIST[i_next][j_next] = DIST[i][j] + 1
                GRAPH[prev_node].add((i_next, j_next), (DIST[i_next][j_next]-DIST[prev_i][prev_j]))
            
            elif M[i_next][j_next] == ' ':
                DIST[i_next][j_next] = DIST[i][j] + 1
                if ((i_next, j_next), prev_node) not in put:
                    Q.put(((i_next, j_next), prev_node))
                    put.add(((i_next, j_next), prev_node))
    
    return Graph(GRAPH, START, END)


def DFS(graph, node, visited):
    if node == graph.end:
        return 0

    max_value = float("-inf")
    visited.add(node)

    for other, value in graph.nodes[node].edges:
        if other not in visited:
            max_value = max(max_value, value + DFS(graph, other, visited))

    visited.remove(node)
    return max_value


def dijkstra(graph):
    dist = {node: float("inf") for node in graph.nodes.keys()}
    path = {node: None for node in graph.nodes.keys()}

    dist[graph.start] = 0
    pq = PriorityQueue()
    pq.put((0, graph.start))

    in_queue = set()
    in_queue.add(graph.start)

    while pq.qsize():
        _, node = pq.get()
        in_queue.remove(node)

        for other, value in graph.nodes[node].edges:
            if dist[node] + value < dist[other]:
                dist[other] = dist[node] + value
                path[other] = node

                if other not in in_queue:
                    pq.put((dist[other], other))
                    in_queue.add(other)

    return -dist[graph.end], path


def part1(inp: list[str]) -> int:
    M = []
    for line in inp:
        M.append([encode[c] for c in line])
    M = np.pad(M, 1, constant_values=('#')).tolist()
    
    graph = generate_graph_2(inp)

    # return dijkstra(graph)
    return DFS(graph, graph.start, set())


def part2(inp: list[str]) -> int:
    return 0


def read_input_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as fin:
        inp = fin.readlines()

    return [line.strip() for line in inp]


if __name__ == '__main__':
    input_str = read_input_file(f"data/input{DAY:02d}.txt")
    input_str = read_input_file(f"data/input00.txt")

    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")
