#!/usr/bin/env python

from aocd import get_data, submit

data = get_data(year=2021, day=9, block=True)
# data = """
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# """.strip()

lines = [[int(c) for c in l] for l in data.split("\n")]

height = len(lines)
width = len(lines[0])

marker = object()
def flood_fill(i, j):
    if lines[i][j] is marker or lines[i][j] == 9:
        return 0

    lines[i][j] = marker

    flooded = 1
    for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if i+y >= 0 and i+y < height and j+x >= 0 and j+x < width:
            target = lines[i+y][j+x]
            if target  != 9 and target != marker:
                flooded += flood_fill(i+y, j+x)
    return flooded

basins = []
for i in range(height):
    for j in range(width):
        size = flood_fill(i, j)
        if size != 0:
            basins.append(size)
p = 1
for _ in range(3):
    m = max(basins)
    p *= m
    basins.remove(m)
print(p)
