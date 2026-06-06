"""

class Graph:
    def __init__(self, mx: list[list[int]]):
        self.adjacency: dict[str, list[tuple[str, int]]] = {}
        self.matrix = mx

    def add_node(self, node: str) -> None:
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, a: str, b: str, weight: int = 1) -> None:
        self.adjacency[a].append((b, weight))
        self.adjacency[a].append((a, weight))

    def neighbors(self, node: str) -> list[tuple[str, int]]:
        return self.adjacency.get(node, [])

 """


def build_graph(mx: list[list[int]]) -> dict:
    graph: dict = {}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    rows, cols = len(mx), len(mx[0])

    for line in range(rows):
        for col in range(cols):
            if (mx[line][col] == 1):
                continue

            node = (line, col)
            graph[node] = []

            for dr, dc in directions:
                nr, nc = line + dr, col + dc
                if (nr >= 0 and nr < rows) and (nc >= 0 and nc < cols):
                    if (mx[nr][nc] != 1):
                        graph[node].append((nr, nc))
    return graph
