
"""
Завдання 3. Алгоритм Дейкстри з використанням бінарної купи (heapq).

Реалізація:
  - Орієнтований/неорієнтований зважений граф через adjacency list.
  - Алгоритм Дейкстри O((V+E) log V) завдяки бінарній купі.
  - Повертає відстані, попередники та дозволяє відновити шлях.

Python 3.10+
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Iterable
import heapq

@dataclass
class Graph:
    directed: bool = False
    # Список суміжності: вершина -> список (сусід, вага)
    adj: Dict[Any, List[Tuple[Any, float]]] = field(default_factory=dict)

    def add_edge(self, u: Any, v: Any, w: float) -> None:
        if w < 0:
            raise ValueError("Алгоритм Дейкстри не працює з від'ємними вагами.")
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])
        if not self.directed:
            self.adj[v].append((u, w))

    def vertices(self) -> List[Any]:
        return list(self.adj.keys())

    def dijkstra(self, source: Any) -> tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
        if source not in self.adj:
            raise KeyError(f"Початкова вершина {source!r} відсутня у графі.")

        dist: Dict[Any, float] = {v: float('inf') for v in self.adj}
        prev: Dict[Any, Optional[Any]] = {v: None for v in self.adj}
        dist[source] = 0.0

        # Мін-купа: (поточна_відстань, вершина)
        heap: list[tuple[float, Any]] = [(0.0, source)]

        visited: set[Any] = set()
        while heap:
            d, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)

            # Якщо ми виймаємо запис із більшим d, ніж дійсний dist[u], пропускаємо
            if d > dist[u]:
                continue

            for v, w in self.adj[u]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        return dist, prev

    def shortest_path(self, source: Any, target: Any) -> list[Any]:
        dist, prev = self.dijkstra(source)
        if dist[target] == float('inf'):
            return []
        # Відновлення шляху
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

if __name__ == "__main__":
    # Демонстрація роботи на невеликому графі
    g = Graph(directed=False)
    edges = [
        ("A","B",4), ("A","C",2),
        ("B","C",1), ("B","D",5),
        ("C","D",8), ("C","E",10),
        ("D","E",2), ("D","Z",6),
        ("E","Z",3),
    ]
    for u,v,w in edges:
        g.add_edge(u,v,w)

    dist, prev = g.dijkstra("A")
    print("Відстані від A:")
    for v in sorted(g.vertices()):
        print(f"  A -> {v}: {dist[v]}")
    print("\nНайкоротший шлях A -> Z:", " -> ".join(g.shortest_path("A","Z")))
