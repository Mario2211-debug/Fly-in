from utils.flyin_types import type_hub, connections
from typing import Dict, Optional


class Conf:
    def __init__(self):
        self.hubs: list[type_hub] = []
        self.end: Optional[type_hub] = None
        self.start: Optional[type_hub] = None
        self.n_drones: int = 0
        self.connections: list[connections] = []

    def get_hub_by_name(self, name: str):
        """Retorna hub pelo nome"""
        if self.start and self.start.name == name:
            return self.start
        if self.end and self.end.name == name:
            return self.end
        for hub in self.hubs:
            if hub.name == name:
                return hub
        return None

    def get_hub_by_coords(self, x: int, y: int):
        """Retorna hub pelas coordenadas"""
        if self.start and self.start.x == x and self.start.y == y:
            return self.start
        if self.end and self.end.x == x and self.end.y == y:
            return self.end
        for hub in self.hubs:
            if hub.x == x and hub.y == y:
                return hub
        return None

    def build_graph(self):
        """
        Constrói o grafo no formato que você já tem:
        { (x, y): [vizinhos] }
        """
        graph = {}

        # Adiciona todos os hubs ao grafo
        all_hubs = [self.start] + self.hubs + [self.end]

        for hub in all_hubs:
            if hub is None:
                continue
            graph[(hub.x, hub.y)] = []

        # Adiciona conexões
        for conn in self.connections:
            hub1 = self.get_hub_by_name(conn.zone1)
            hub2 = self.get_hub_by_name(conn.zone2)

            if hub1 and hub2:
                graph[(hub1.x, hub1.y)].append((hub2.x, hub2.y))
                graph[(hub2.x, hub2.y)].append((hub1.x, hub1.y))

        return graph



def parse_options(options_list: list) -> Dict[str, Optional[str]]:
    """Parses a list of options like ['[zone=normal]',
    '[color=red]'] into a dict"""
    options_dict = {}
    for op in options_list:
        op = op.strip("[]")
        if "=" in op:
            key, value = op.split("=", 1)  # max 1 split
            options_dict[key] = value
        else:
            options_dict[op] = None
    return options_dict


def parser(file) -> Conf:
    """Parse the input file and return a Conf object"""
    data = file.readlines()
    conf = Conf()

    for line_num, line in enumerate(data, 1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        try:
            if line.startswith("nb_drones:"):
                _, value = line.split(":", 1)
                conf.n_drones = int(value.strip())

            elif line.startswith("start_hub:"):
                _, values = line.split(":", 1)
                parts = values.strip().split()

                if len(parts) < 3:
                    raise ValueError(f"Line {line_num}: "
                                     "start_hub requires name x y")

                name = parts[0]
                x = int(parts[1])
                y = int(parts[2])
                options = parts[3:] if len(parts) > 3 else []

                conf.start = type_hub(name, x, y, parse_options(options))

            elif line.startswith("end_hub:"):
                _, values = line.split(":", 1)
                parts = values.strip().split()

                if len(parts) < 3:
                    raise ValueError(f"Line {line_num}: "
                                     "end_hub requires name x y")

                name = parts[0]
                x = int(parts[1])
                y = int(parts[2])
                options = parts[3:] if len(parts) > 3 else []

                conf.end = type_hub(name, x, y, parse_options(options))

            elif line.startswith("hub:"):
                _, values = line.split(":", 1)
                parts = values.strip().split()

                if len(parts) < 3:
                    raise ValueError(f"Line {line_num}: hub requires name x y")

                name = parts[0]
                x = int(parts[1])
                y = int(parts[2])
                options = parts[3:] if len(parts) > 3 else []

                conf.hubs.append(type_hub(name, x, y, parse_options(options)))

            elif line.startswith("connection:"):
                _, values = line.split(":", 1)
                parts = values.strip().split()

                if len(parts) < 1:
                    raise ValueError(f"Line {line_num}: "
                                     "connection requires name")

                name = parts[0]
                options = parts[1:] if len(parts) > 1 else []

                # Validate connection name format (zone1-zone2)
                if "-" not in name:
                    raise ValueError(f"Line {line_num}: connection name"
                                     f" must be 'zone1-zone2', got '{name}'")

                conf.connections.append(
                    connections(name, parse_options(options)))

            else:
                pass

        except ValueError as e:
            print(f"Parser error at line {line_num}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error at line {line_num}: {e}")
            raise

    # Validation after parsing
    if conf.n_drones <= 0:
        raise ValueError("nb_drones must be positive")

    if conf.start is None:
        raise ValueError("start_hub not found")

    if conf.end is None:
        raise ValueError("end_hub not found")

    return conf
