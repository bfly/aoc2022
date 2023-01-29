import re
import time
import itertools


def read_puzzle(file):
    with open(file) as f:
        return [re.findall('[A-Z]+|\d+', line[1:]) for line in f.readlines()]


def solve(puzzle):
    graph = {valve: leads for valve, _, *leads in puzzle}
    flows = {valve: int(flow) for valve, flow, *_ in puzzle if flow != '0'}
    indices = {valve: 1 << i for i, valve in enumerate(flows)}
    distances = {(v, l): 1 if l in graph[v] else 1000 for l in graph for v in graph}

    # floyd-warshall = Distance for any possible pair of valves
    for k, i, j in itertools.permutations(graph, 3):
        distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])

    def visit(valve, minutes, bitmask, pressure, answer):
        answer[bitmask] = max(answer.get(bitmask, 0), pressure)
        for valve2, flow in flows.items():
            remaining_minutes = minutes - distances[valve, valve2] - 1
            if indices[valve2] & bitmask or remaining_minutes <= 0: continue
            visit(valve2, remaining_minutes, bitmask | indices[valve2], pressure + flow * remaining_minutes, answer)
        return answer

    part1 = max(visit('AA', 30, 0, 0, {}).values())
    visited2 = visit('AA', 26, 0, 0, {})
    part2 = max(v1 + v2 for bitmask1, v1 in visited2.items()
                for bitmask2, v2 in visited2.items() if not bitmask1 & bitmask2)
    return part1, part2


fn1 = "../data/day16/test.txt"
fn2 = "../data/day16/input.txt"

time_start = time.perf_counter()
print(solve(read_puzzle(fn2)))
print(time.perf_counter() - time_start)
