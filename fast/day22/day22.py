#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from aocd import get_data, submit

data = get_data(year=2021, day=22, block=True)

import re

volumes = []
for line in data.splitlines():
    m = re.match(r"(\w+) x=(-?\d+..-?\d+),y=(-?\d+..-?\d+),z=(-?\d+..-?\d+)", line)
    add = m.group(1) == "on"
    x = m.group(2)
    y = m.group(3)
    z = m.group(4)
    x1, x2 = tuple(map(int, x.split("..")))
    y1, y2 = tuple(map(int, y.split("..")))
    z1, z2 = tuple(map(int, z.split("..")))

    volumes.append(((x1, x2+1), (y1, y2+1), (z1, z2+1), add))


from collections import defaultdict

cuboids = []

for v1 in volumes:
    (v1x1, v1x2), (v1y1, v1y2), (v1z1, v1z2), add = v1

    intersections = []
    for v2 in cuboids:
        (v2x1, v2x2), (v2y1, v2y2), (v2z1, v2z2), flavour = v2

        ix1, ix2 = max(v1x1, v2x1), min(v1x2, v2x2)
        iy1, iy2 = max(v1y1, v2y1), min(v1y2, v2y2)
        iz1, iz2 = max(v1z1, v2z1), min(v1z2, v2z2)
        if ix1 <= ix2 and iy1 <= iy2 and iz1 <= iz2:
            overlap = ((ix1, ix2), (iy1, iy2), (iz1, iz2), not flavour)
            intersections.append(overlap)
    cuboids.extend(intersections)
    if add:
        cuboids.append(v1)


v = 0
for c in cuboids:
    x, y, z, flavour = c
    volume = (x[1]-x[0])*(y[1]-y[0])*(z[1]-z[0])
    if flavour:
        v += volume
    else:
        v -= volume
print(v)
