from dataclasses import dataclass
from enum import Enum


class type_zone(str, Enum):
    normal = "normal",
    blocked = "blocked",
    restricted = "restricted",
    priority = "priority"


@dataclass
class connections:
    name: str
    options: list[dict, ...]


@dataclass
class type_hub:
    name: str
    x: int
    y: int
    options: list[dict]


@dataclass
class zone:
    name: str
    start: int
    end: int
    hub: int
    zone_type: type_zone


@dataclass
class map_type:
    nb_drones: int
    start_hub: type_hub
    hub: type_hub
    end_hub: type_hub
    conn: connections
