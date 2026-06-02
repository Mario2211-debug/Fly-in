
class Drones:
    def __init__(self, alias: str):
        self.name: str = alias
        self.drones: list = []
        pass

    def create_drones(self, nbr: int) -> list:
        self.drones = [self.name + f"{i}" for i in range(0, nbr)]
        return self.drones

    def show(self):
        for drone in self.drones:
            print(f"{drone}")
