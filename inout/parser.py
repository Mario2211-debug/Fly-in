from utils.fly_types import type_hub, connections


class Conf:
    def __init__(self):
        self.hubs: list[type_hub] = []
        self.end = None
        self.start = None
        self.n_drones = 0
        self.connections = []
    pass


def parser(file) -> Conf:
    data = file.readlines()
    conf = Conf()

    for line in data:
        line = line.strip()
        if line.startswith("#"):
            continue

        elif line.startswith("nb_drones:"):
            key, value = line.split(":")
            conf.n_drones = int(value)

        elif line.startswith("start_hub:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            x = parts[1]
            y = parts[2]
            options = parts[3:]
            print(options[0].strip().split("="))
            conf.start = type_hub(name, x, y, options)

        elif line.startswith("hub:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            x = parts[1]
            y = parts[2]
            options = parts[3:]
            conf.hubs.append(type_hub(name, int(x), int(y), options))

        elif line.startswith("end_hub:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            x = parts[1]
            y = parts[2]
            options = parts[3:]
            conf.end = type_hub(name, x, y, [options])

        elif line.startswith("connection:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            options = parts[1:]
            conf.connections.append(connections(name, options))

    return conf
