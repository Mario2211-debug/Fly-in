# core/simulation.py
from typing import List, Dict, Tuple, Optional, Set
from utils.flyin_types import type_hub, connections, Drone
from core.pathfinding import PathFinder


class Simulation:
    def __init__(self, conf):
        self.conf = conf
        self.pathfinder = PathFinder(conf)
        self.drones: List[Drone] = []
        self.turn = 0
        self.output_lines: List[str] = []

        # Estado atual
        self.zone_occupancy: Dict[str, int] = {}  # nome do hub -> número de drones
        self.link_usage: Dict[str, int] = {}      # nome da conexão -> uso neste turno

        # Inicializa drones
        self._init_drones()

        # Pré-computa caminhos para todos os drones
        self._precompute_paths()

    def _init_drones(self):
        """Cria todos os drones na posição inicial"""
        start_pos = (self.conf.start.x, self.conf.start.y)
        for i in range(self.conf.n_drones):
            drone = Drone(
                id=i + 1,
                current_zone=self.conf.start.name,
                current_pos=start_pos
            )
            self.drones.append(drone)

        # Ocupação inicial da start zone (capacidade infinita)
        self.zone_occupancy[self.conf.start.name] = self.conf.n_drones

    def _precompute_paths(self):
        """Calcula caminho mínimo para cada drone (do start ao end)"""
        start_pos = (self.conf.start.x, self.conf.start.y)
        end_pos = (self.conf.end.x, self.conf.end.y)

        path, cost = self.pathfinder.shortest_path(start_pos, end_pos)

        if path is None:
            raise RuntimeError(f"No path from start to end!")

        # Converte posições para nomes de hubs
        path_names = []
        for pos in path:
            hub = self.pathfinder.get_hub_at(pos)
            if hub:
                path_names.append(hub.name)

        # Todos os drones seguem o mesmo caminho (depois melhoramos)
        for drone in self.drones:
            drone.path = path_names[1:]  # exclui posição atual

    def _get_drone_position_index(self, drone: Drone) -> int:
        """Retorna índice atual do drone no caminho"""
        if drone.delivered:
            return len(drone.path)
        for i, zone in enumerate(drone.path):
            if zone == drone.current_zone:
                return i
        return -1

    def _can_move(self, drone: Drone, target_zone_name: str) -> bool:
        """Verifica se drone pode mover para target_zone"""
        target_hub = self.conf.get_hub_by_name(target_zone_name)

        if not target_hub:
            return False

        # Verifica se é blocked
        if target_hub.is_blocked:
            return False

        # Verifica capacidade da zona (exceto start e end)
        current_occupancy = self.zone_occupancy.get(target_zone_name, 0)
        if target_hub.max_drones <= current_occupancy:
            if target_zone_name != self.conf.end.name:
                return False

        # Verifica conexão
        conn_name = f"{drone.current_zone}-{target_zone_name}"
        conn_rev = f"{target_zone_name}-{drone.current_zone}"

        conn = None
        for c in self.conf.connections:
            if c.name == conn_name or c.name == conn_rev:
                conn = c
                break

        if conn:
            current_link_usage = self.link_usage.get(conn.name, 0)
            if current_link_usage >= conn.max_link_capacity:
                return False

        return True

    def _try_move_drone(self, drone: Drone) -> Optional[str]:
        """Tenta mover drone para próximo passo do caminho"""
        if drone.delivered:
            return None

        idx = self._get_drone_position_index(drone)

        if idx + 1 >= len(drone.path):
            # Chegou ao destino
            if drone.current_zone == self.conf.end.name:
                drone.delivered = True
                self.zone_occupancy[drone.current_zone] = max(0, self.zone_occupancy.get(drone.current_zone, 0) - 1)
                return None
            return None

        target_zone = drone.path[idx + 1]

        if self._can_move(drone, target_zone):
            return target_zone

        return None  # não pode mover, fica

    def _resolve_moves(self) -> Dict[int, str]:
        """Resolve movimentos para todos os drones neste turno"""
        moves = {}

        # Ordena drones por prioridade (mais perto do goal primeiro)
        sorted_drones = sorted(self.drones, key=lambda d: self._get_drone_position_index(d), reverse=True)

        for drone in sorted_drones:
            if drone.delivered:
                continue

            target = self._try_move_drone(drone)
            if target:
                moves[drone.id] = target

        return moves

    def _apply_moves(self, moves: Dict[int, str]):
        """Aplica os movimentos aprovados"""
        # Primeiro, remove drones das zonas atuais
        for drone_id, target in moves.items():
            drone = self.drones[drone_id - 1]
            # Libera zona atual
            self.zone_occupancy[drone.current_zone] = max(0, self.zone_occupancy.get(drone.current_zone, 0) - 1)

        # Depois, adiciona nas novas zonas
        for drone_id, target in moves.items():
            drone = self.drones[drone_id - 1]
            drone.current_zone = target

            # Atualiza posição (precisa do hub para coordenadas)
            hub = self.conf.get_hub_by_name(target)
            if hub:
                drone.current_pos = (hub.x, hub.y)

            self.zone_occupancy[target] = self.zone_occupancy.get(target, 0) + 1

    def _record_turn(self, moves: Dict[int, str]):
        """Registra output do turno"""
        if moves:
            move_strs = [f"D{drone_id}-{zone}" for drone_id, zone in sorted(moves.items())]
            self.output_lines.append(" ".join(move_strs))
        else:
            self.output_lines.append("")  # turno sem movimentos

    def _all_delivered(self) -> bool:
        return all(drone.delivered for drone in self.drones)

    def run(self) -> List[str]:
        """Executa a simulação completa"""
        self.output_lines = []  # reset

        while not self._all_delivered():
            self.turn += 1
            self.link_usage = {}  # reseta uso de conexões para este turno

            moves = self._resolve_moves()
            self._apply_moves(moves)
            self._record_turn(moves)

            # Segurança: evita loop infinito
            if self.turn > 10000:
                print("Warning: Max turns reached!")
                break

        return self.output_lines

    def get_stats(self) -> Dict:
        """Retorna estatísticas da simulação"""
        return {
            "total_turns": self.turn,
            "drones_delivered": sum(1 for d in self.drones if d.delivered),
            "total_drones": len(self.drones)
        }
