import heapq


def dfs(graph: dict, start: tuple, end: None) -> None:
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if (end is not None) and node == end:
            return path
        if node not in visited:
            visited.add(node)
            # print(f"{node} caminho: {path}")

            for nbh in reversed(graph[node]):
                if nbh not in visited:
                    stack.append((nbh, path + [nbh]))
    print(f"{stack}\n")
    return None


def dijkstra(graph, start, end):

    dist = {no: float('inf') for no in graph}
    dist[start] = 0
    pred = {no: None for no in graph}
    heap = [(0, start)]

    while heap:
        curr_dist, curr = heapq.heappop(heap)

        if curr_dist > dist[curr]:
            continue

        if curr == end:
            break

        for neighbor in graph[curr]:
            new_dist = curr_dist + 1

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                pred[neighbor] = curr
                heapq.heappush(heap, (new_dist, neighbor))

    if end not in pred or (pred[end] is None and end != start):
        return None, float('inf')

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = pred[curr]
    path.reverse()

    if path[0] == start:
        return path, dist[end]
    else:
        return None, float('inf')
