#!/usr/bin/env python

from collections import defaultdict
import heapq

from aocd import get_data, submit
from aoc_utils import Grid

import sys
sys.setrecursionlimit(5000)

data = get_data(year=2021, day=15, block=True)
# data = """
# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581
# """.strip()

rows = data.splitlines()
gg = [[int(c) for c in row] for row in rows]
lc = len(gg)
lr = len(gg[0])

# grid = [[int(c) for c in row] for row in data.splitlines()]
grid = [[0 for _ in range(lr*5)] for _ in range(lc*5)]

for yy in range(5):
    for xx in range(5):
        for y in range(lc):
            for x in range(lr):
                original = gg[y%lc][x%lr]
                v = original
                for inc in range(yy+xx):
                    v += 1
                    if v > 9:
                        v = 1
                idxy = y+yy*lc 
                idxx = x+xx*lr 
                grid[idxy][idxx] = v

grid = Grid(grid)
graph = defaultdict(set)

for y in range(5*lc):
    for x in range(5*lr):
        for p, v in grid.around_with_index((y, x), corners=False):
            graph[(y, x)].add((p, v))

def dijkstra(graph, source):
    inf = float('inf')
    dist = { source: 0 }
    pq = [(0, source)]
    history = set()

    while pq:
        _, u = heapq.heappop(pq)
        if u in history:
            continue
        history.add(u)
        for conn in graph[u]:
            v, cost = conn
            if v in history:
                continue

            alt = dist[u] + cost
            if alt < dist.get(v, inf):
                dist[v] = alt
                heapq.heappush(pq, (alt, v))

    return dist

dist = dijkstra(graph, (0, 0))
print(dist[grid.height - 1, grid.width - 1])
