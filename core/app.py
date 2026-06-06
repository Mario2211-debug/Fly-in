from inout.parser import parser
from core.drones import Drones
from core.build_graph import build_graph
from utils.matrix import matrix
from utils.algorithms import dijkstra


def app():
    file = open("./maps/hard/01_maze_nightmare.txt", "r")
    config = parser(file)
    graph = build_graph(matrix)
    drone = Drones("DM")
    drone.create_drones(7)

    for data in graph:
        print(f"{data}: {graph[data]}\n")

    print("Start Hubs: ")
    print(f"{config.start.name}: {config.start.options}")
    print("\n")
    print("Hubs: ")
    for hub in config.hubs:
        print(f"{hub.name}: {hub.options}")
    print("\n")

    print("End Hubs: ")
    print(f"{config.end.name}: {config.end.options}")
    print("\n")

    print("Connections: ")
    for conn in config.connections:
        print(f"{conn.name}: {conn.options}")

    # print(graph.keys())
    print("DFS a partir do vértice 0:")

    caminho, custo = dijkstra(graph, (1, 1), (18, 7))
    print(f"Menor caminho: {caminho} com custo {custo}")
