import re
from abc import ABC, abstractmethod
from collections import deque
from contextlib import suppress
from dataclasses import dataclass
from functools import cached_property
from heapq import heappush, heappop
from itertools import permutations
from typing import Any, Final, Iterator, NamedTuple, Self

LINE: Final[re.Pattern[str]] = re.compile(
    r"^Valve (?P<name>[A-Z]{2}) has flow rate=(?P<rate>\d+); "
    r"(?:tunnels lead to valves|tunnel leads to valve) (?P<valves>[A-Z, ]*)$"
)


class Valve(NamedTuple):
    name: str
    rate: int
    valves: frozenset[str]

    @classmethod
    def from_line(cls, line: str) -> Self:
        match = LINE.match(line)
        assert match is not None
        rate = int(match["rate"])
        valves = frozenset(v.strip() for v in match["valves"].split(","))
        return cls(match["name"], rate, valves)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.name}, {self.rate}, "
            f"[{','.join(sorted(self.valves))}])"
        )


@dataclass
class TunnelStep:
    valve: Valve
    time_left: int = 30
    total_released: int = 0
    visited: frozenset[Valve] = frozenset()

    def traverse(self, graph: "Graph") -> Iterator[Self]:
        for valve, steps in graph.distances[self.valve].items():
            if valve in self.visited or not valve.rate:
                # either we already opened the valve here, or it is not worth
                # stopping here as the effect would be 0.
                continue
            if (time_left := self.time_left - steps - 1) <= 0:
                # no point in going here, the result would be 0.
                continue
            yield __class__(
                valve,
                time_left,
                self.total_released + valve.rate * time_left,
                self.visited | {valve},
            )


class Graph:
    def __init__(self, nodes: dict[str, Valve]):
        self.nodes = nodes

    @classmethod
    def from_text(cls, text: str) -> Self:
        return cls({(v := Valve.from_line(line)).name: v for line in text.splitlines()})

    @cached_property
    def distances(self) -> dict[Valve, dict[Valve, int]]:
        """Minimal distances to move from one valve to another

        Uses the Floyd-Warshall algorithm to find the minimum distances from
        any node in the graph to any other node.
        """
        graph = self.nodes
        dist: dict[Valve, dict[Valve, int]] = {v: {graph[n]: 1 for n in v.valves} for v in graph.values()}
        max = len(graph)
        for k, i, j in permutations(graph.values(), r=3):
            with suppress(KeyError):
                dist[i][j] = min(dist[i][k] + dist[k][j], dist[i].get(j, max))
        return dist

    def max_pressure_reliefs(self, remaining: int = 30) -> dict[frozenset[Valve], int]:
        max_relief: dict[frozenset[Valve], int] = {}
        queue = deque([TunnelStep(self.nodes["AA"], remaining)])
        while queue:
            node = queue.popleft()
            for new in node.traverse(self):
                max_relief[new.visited] = max(max_relief.get(new.visited, 0), new.total_released)
                queue.append(new)
        return max_relief

    def optimise_pressure_relief(self) -> int:
        return max(self.max_pressure_reliefs().values())
