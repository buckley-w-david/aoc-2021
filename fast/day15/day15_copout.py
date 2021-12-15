#!/usr/bin/env python

# Day 15 but I gave up trying to solve it myself and just used a library

from aocd import get_data, submit
from aoc_utils import Grid

from dijkstar import Graph, find_path

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
                original = gg[y][x]
                v = original
                for inc in range(yy+xx):
                    v += 1
                    if v > 9:
                        v = 1
                grid[y+yy*lc][x+xx*lr] = v

grid = Grid(grid)
graph = Graph()

for y in range(5*lc):
    for x in range(5*lr):
        for p, v in grid.around_with_index((y, x), corners=False):
            graph.add_edge((y, x), p, v)

print(find_path(graph, (0, 0), (lc*5 - 1, lr * 5 - 1)))
