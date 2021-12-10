#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2021, day=7, block=True)
# data = "16,1,2,0,4,2,7,1,2,14"

pos = [int(l) for l in data.split(",")]

min_fuel = None
for position in range(min(pos), max(pos)):
    fuel = 0
    for p in pos:
        distance = abs(position - p)
        fuel += distance*(distance+1)//2
    if min_fuel is None or fuel < min_fuel:
        min_fuel = fuel

print(min_fuel)
