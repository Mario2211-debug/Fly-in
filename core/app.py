from inout.parser import parser
from core.drones import Drones


def app():
    data = open("./maps/easy/03_basic_capacity.txt", "r")
    config = parser(data)
    drone = Drones("DM")
    drone.create_drones(7)

    for conn in config.connections:
        print(conn.name)
    print("\n")
    for hub in config.hubs:
        print(hub.name)