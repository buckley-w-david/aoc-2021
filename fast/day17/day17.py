#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from aocd import get_data, submit

data = get_data(year=2021, day=17, block=True)
data = """
target area: x=29..73, y=-248..-194
""".strip()

# data = "target area: x=20..30, y=-10..-5"
print(data)
import re

target = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", data)

x0, x1 = int(target.group(1)), int(target.group(2))
y0, y1 = int(target.group(3)), int(target.group(4))

print(x0, x1, y0, y1)

x = 0
y = 0

x_dir = x0 > 0
y_dir = y0 > 0

old_max_y = -1
max_y = -1

ys = set()
for dx in range(0, 1000):
    for dy in range(-500, 500):
        ddx = dx
        ddy = dy
        x, y = 0, 0
        while x < x1 and y > y0:
            x += ddx
            y += ddy

            if y > max_y:
                max_y = y

            ddx = max(ddx - 1, 0)
            ddy -= 1

            if (x0 <= x <= x1 and y0 <= y <= y1):
                break
        else:
            max_y = old_max_y
            continue
        old_max_y = max_y
        ys.add((dx, dy))

print(len(ys))
