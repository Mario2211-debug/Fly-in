class Drone:
    def __init__(self, name: str, path: list):
        self.name = name
        self.path = path
        self.step = 0
        self.status = "moving"
        self.link_atual = None

    @property
    def position(self):
        return self.path[self.step]

    @property
    def next_position(self):
        if self.step + 1 < len(self.path):
            return self.path[self.step + 1]
        return None

    def advance(self, link=None):
        self.link_atual = link
        self.step += 1
        if self.step == len(self.path) - 1:
            self.status = "done"

    def wait(self):
        self.status = "waiting"


class Drones:
    def __init__(self, n: int, path: list, conf):
        self.drones = [Drone(f"drone{i}", path) for i in range(n)]
        self.conf = conf
        self.turno = 0

        # ocupacao por nó — chave é type_hub
        all_hubs = [conf.start] + conf.hubs + [conf.end]
        self.ocupacao: dict = {hub: 0 for hub in all_hubs}
        self.ocupacao[conf.start] = n  # todos começam no start

        # ocupacao por aresta — chave é (type_hub, type_hub)
        self.link_ocupacao: dict = {}
        for conn in conf.connections:
            h1 = conf.get_hub_by_name(conn.zone1)
            h2 = conf.get_hub_by_name(conn.zone2)
            if h1 and h2:
                self.link_ocupacao[(h1, h2)] = 0
                self.link_ocupacao[(h2, h1)] = 0

    def _get_link(self, pos_atual, pos_prox):
        """retorna a conexão entre dois hubs"""
        h1 = self.conf.get_hub_by_coords(*pos_atual)
        h2 = self.conf.get_hub_by_coords(*pos_prox)
        for conn in self.conf.connections:
            if (conn.zone1 == h1.name and conn.zone2 == h2.name or
                conn.zone2 == h1.name and conn.zone1 == h2.name):
                return conn, h1, h2
        return None, h1, h2

    def _pode_avancar(self, drone: Drone) -> bool:
        """verifica capacidade do nó e da aresta"""
        prox = drone.next_position
        if prox is None:
            return False

        hub_prox = self.conf.get_hub_by_coords(*prox)
        if hub_prox is None:
            return False

        # verifica capacidade do nó
        if self.ocupacao[hub_prox] >= hub_prox.max_drones:
            return False

        # verifica capacidade da aresta
        conn, h1, h2 = self._get_link(drone.position, prox)
        if conn and self.link_ocupacao.get((h1, h2), 0) >= conn.max_link_capacity:
            return False

        return True

    def _step(self):
        # 1. liberta arestas do turno anterior
        for drone in self.drones:
            if drone.link_atual:
                self.link_ocupacao[drone.link_atual] -= 1
                drone.link_atual = None

        # 2. processa movimentos
        for drone in self.drones:
            if drone.status == "done":
                continue

            if self._pode_avancar(drone):
                conn, h1, h2 = self._get_link(drone.position,
                                              drone.next_position)

                self.ocupacao[h1] -= 1
                self.ocupacao[h2] += 1

                if conn:
                    self.link_ocupacao[(h1, h2)] += 1
                    drone.advance((h1, h2))  # passa a aresta usada
                else:
                    drone.advance(None)

                print(f"  {drone.name}: {h1.name} → {h2.name}")
            else:
                drone.wait()
                print(f"  {drone.name}: aguarda em {drone.position}")

    def run(self):
        while not all(d.status == "done" for d in self.drones):
            self.turno += 1
            print(f"\n--- Turno {self.turno} ---")
            self._step()

            # proteção contra loop infinito
            if self.turno > 1000:
                print("ERRO: possível deadlock")
                break

        print(f"\nTodos os drones chegaram em {self.turno} turnos!")