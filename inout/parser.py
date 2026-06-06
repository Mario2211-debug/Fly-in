from utils.flyin_types import type_hub, connections


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

            options_dict = {}
            for op in options:
                op = op.strip("[]")
                if "=" in op:
                    key, value = op.split("=")
                    options_dict[key] = value
                else:
                    options_dict[key] = None
            conf.start = type_hub(name, x, y, options_dict)

        elif line.startswith("hub:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            x = parts[1]
            y = parts[2]
            options = parts[3:]

            options_dict = {}
            for op in options:
                op = op.strip("[]")
                if "=" in op:
                    key, value = op.split("=")
                    options_dict[key] = value
            conf.hubs.append(type_hub(name, int(x), int(y), options_dict))

        elif line.startswith("end_hub:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            x = parts[1]
            y = parts[2]
            options = parts[3:]

            options_dict = {}
            for op in options:
                op = op.strip("[]")
                if "=" in op:
                    key, value = op.split("=")
                    options_dict[key] = value
                else:
                    options_dict[key] = None
            conf.end = type_hub(name, x, y, options_dict)

        elif line.startswith("connection:"):
            _, values = line.split(":")
            parts = values.strip().split()
            name = parts[0]
            options = parts[1:]

            options_dict = {}
            for op in options:
                op = op.strip("[]")
                if "=" in op:
                    key, value = op.split("=")
                    options_dict[key] = value
                else:
                    options_dict[key] = None
            conf.connections.append(connections(name,  options_dict))
    return conf
