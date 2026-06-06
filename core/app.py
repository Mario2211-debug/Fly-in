from inout.parser import parser
from core.drones import Drones


def app():
    data = open("./maps/hard/01_maze_nightmare.txt", "r")
    config = parser(data)
    drone = Drones("DM")
    drone.create_drones(7)

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
