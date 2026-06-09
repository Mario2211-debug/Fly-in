# utils/flyin_types.py
from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class type_hub:
    name: str
    x: int
    y: int
    options: Dict[str, Any] = field(default_factory=dict, hash=False, compare=False)

    def __hash__(self):
        return hash((self.name, self.x, self.y))

    @property
    def zone_type(self) -> str:
        """zone normal, restricted, priority, or blocked"""
        val = self.options.get("zone")
        if val is None:
            return "normal"
        return str(val)

    @property
    def color(self) -> Optional[str]:
        """color name or None"""
        val = self.options.get("color")
        if val is None:
            return None
        return str(val)

    @property
    def max_drones(self) -> int:
        """maximum drones in this zone (default 1)"""
        val = self.options.get("max_drones")
        if val is None:
            return 1
        try:
            return int(val)
        except (ValueError, TypeError):
            return 1

    @property
    def movement_cost(self) -> int:
        """cost in turns to enter this zone"""
        if self.zone_type == "restricted":
            return 2
        # priority e normal custam 1
        return 1

    @property
    def is_blocked(self) -> bool:
        return self.zone_type == "blocked"


@dataclass
class connections:
    name: str  # format: "zone1-zone2"
    options: Dict[str, Any] = field(default_factory=dict)

    @property
    def zone1(self) -> str:
        return self.name.split("-")[0]

    @property
    def zone2(self) -> str:
        return self.name.split("-")[1]

    @property
    def max_link_capacity(self) -> int:
        val = self.options.get("max_link_capacity")
        if val is None:
            return 1
        try:
            return int(val)
        except (ValueError, TypeError):
            return 1
