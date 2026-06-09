from dataclasses import dataclass


@dataclass
class Snapshot:
    turn: int
    drone_positions: dict   # {drone_name: (x,y)}
    node_occupancy: dict    # {hub: count}
    edge_usage: dict        # {(hub1, hub2): count}