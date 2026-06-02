from drones import Drones
from fly_types import type_hub, connections


data = open("maps/easy/03_basic_capacity.txt", "r")


class Maps:
    def __init__(self):
        self.hubs: list[type_hub] = []
        self.end = type_hub
        self.start = type_hub
        self.n_drones = 0
        self.connections: list[connections] = []

    def show(self):
        pass
    pass


def parser(file) -> Maps:
    data = file.readlines()
    ext = Maps()

    for line in data:
        line = line.strip()
        if line.startswith("#"):
            continue

        elif line.startswith("nb_drones:"):
            key, value = line.split(":")
            ext.n_drones = int(value)

        elif line.startswith("start_hub:"):
            key, values = line.split(":")
            _, name, x, y, options = values.split(" ")
            ext.start.name = str(name)
            ext.start.x = int(x)
            ext.start.y = int(y)
            ext.start.options = options

        elif line.startswith("hub:"):
            key, values = line.split(":")
            _, name, x, y, options = values.split(" ")
            ext.hubs.append(type_hub(name, int(x), int(y), [options]))

        elif line.startswith("end_hub:"):
            key, values = line.split(":")
            _, name, x, y, options = values.split(" ")
            ext.end.name = str(name)
            ext.end.x = int(x)
            ext.end.y = int(y)
            ext.end.options = options

        elif line.startswith("connection:"):
            key, values = line.split(":")
            _, name = values.split(" ")
            ext.connections.append(connections(name, _))

    return ext


def main():
    config = parser(data)
    drone = Drones("DM")
    drone.create_drones(7)

    for conn in config.connections:
        print(conn.name)
    print("\n")
    for hub in config.hubs:
        print(hub.name)


if __name__ == "__main__":
    main()
