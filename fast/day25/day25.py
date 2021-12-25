#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from aocd import get_data, submit

data = get_data(year=2021, day=25, block=True)
# data = """
# v...>>.vv>
# .vv>>.vv..
# >>.>v>...v
# >>v>>.>.v.
# v>v.vv.v..
# >.>>..v...
# .vv..>.>v.
# v.v..>>v.v
# ....v..v.>
# """.strip()

lines = data.splitlines()
height = len(lines)
width = len(lines[0])

east_herd = set()
south_herd = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == 'v':
            south_herd.add((y, x))
        elif char == '>':
            east_herd.add((y, x))

i = 0
while True:
    i += 1
    moved = False
    can_move = set()
    for y, x in east_herd:
        n = (y, (x+1) % width)
        if n not in east_herd and n not in south_herd:
            moved = True
            can_move.add((y, x))

    for y, x in can_move:
        east_herd.remove((y, x))
        east_herd.add((y, (x+1) % width))

    can_move = set()
    for y, x in south_herd:
        n = ((y+1)%height, x)
        if n not in east_herd and n not in south_herd:
            moved = True
            can_move.add((y, x))

    for y, x in can_move:
        south_herd.remove((y, x))
        south_herd.add(((y+1)%height, x))

    if not moved:
        break
print(i)
