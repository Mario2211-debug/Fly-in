# core/pathfinding.py
import heapq
from typing import Dict, List, Tuple, Optional, Any
from utils.flyin_types import type_hub, connections


class PathFinder:
    def __init__(self, conf):
        self.conf = conf
        self.graph = self._build_graph()

    def _build_graph(self) -> Dict[Tuple[int, int],
                                   List[Tuple[Tuple[int, int], int]]]:
        """Constrói grafo com pesos baseados no zone_type"""
        graph: dict = {}

        # Adiciona todos os hubs
        all_hubs = []
        if self.conf.start:
            all_hubs.append(self.conf.start)
        all_hubs.extend(self.conf.hubs)
        if self.conf.end:
            all_hubs.append(self.conf.end)

        for hub in all_hubs:
            if not hub.is_blocked:
                graph[(hub.x, hub.y)] = []

        # Adiciona conexões com peso
        for conn in self.conf.connections:
            hub1 = self.conf.get_hub_by_name(conn.zone1)
            hub2 = self.conf.get_hub_by_name(conn.zone2)

            if hub1 and hub2 and not hub1.is_blocked and not hub2.is_blocked:
                # Peso baseado no tipo do hub de destino
                weight = hub2.movement_cost
                graph[(hub1.x, hub1.y)].append(((hub2.x, hub2.y), weight))
                graph[(hub2.x, hub2.y)].append(((hub1.x, hub1.y),
                                                hub1.movement_cost))

        return graph

    def shortest_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
        """Retorna (caminho, custo_total) usando Dijkstra"""
        if start not in self.graph:
            return None, float('inf')
        if end not in self.graph:
            return None, float('inf')

        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0
        pred = {node: None for node in self.graph}
        heap = [(0, start)]
        visited = set()

        while heap:
            current_dist, current = heapq.heappop(heap)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                break

            for neighbor, weight in self.graph.get(current, []):
                new_dist = current_dist + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    pred[neighbor] = current
                    heapq.heappush(heap, (new_dist, neighbor))

        # Reconstrói caminho
        if dist[end] == float('inf'):
            return None, float('inf')

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = pred[current]
        path.reverse()

        return path, dist[end]

    def get_hub_at(self, pos: Tuple[int, int]) -> Optional[type_hub]:
        """Retorna o hub nas coordenadas (x, y)"""
        if self.conf.start and (self.conf.start.x, self.conf.start.y) == pos:
            return self.conf.start
        if self.conf.end and (self.conf.end.x, self.conf.end.y) == pos:
            return self.conf.end
        for hub in self.conf.hubs:
            if (hub.x, hub.y) == pos:
                return hub
        return None
