from utils.flyin_types import zone


class Zones:
    def __init__(self, name: str, start: zone, end: zone, hub):
        self.name: str = name
        self.drones: list = []
        pass

    def rules(self):
        pass

    def create_zones(self, nbr: int) -> list:
        self.drones = [self.name + f"{i}" for i in range(0, nbr)]
        return self.drones

    def show(self):
        for drone in self.drones:
            print(f"{drone}")
