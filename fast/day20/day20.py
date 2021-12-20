#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from pprint import pprint
from aocd import get_data, submit
from aoc_utils import Grid
import numpy as np

data = get_data(year=2021, day=20, block=True)

algorithm, input_image = data.split("\n\n")
algorithm = [c == '#' for c in algorithm]

output = set()
for y, row in enumerate(input_image.split("\n")):
    for x, col in enumerate(row):
        if col == '#':
            output.add((y, x)) 

def display(img):
    my, _ = max(img, key=lambda p: p[0])
    _, mx = max(img, key=lambda p: p[1])

    mmy, _ = min(img, key=lambda p: p[0])
    _, mmx = min(img, key=lambda p: p[1])
    for y in range(mmy, my+1):
        for x in range(mmx, mx+1):
            if (y, x) in img:
                print('#', end='')
            else:
                print('.', end='')
        print()

def around(p):
    y, x = p
    for yy in range(-1, 2):
        for xx in range(-1, 2):
            yield (y+yy, x+xx)

outside = False
for c in range(50):
    max_y, _ = max(output, key=lambda p: p[0])
    _, max_x = max(output, key=lambda p: p[1])

    min_y, _ = min(output, key=lambda p: p[0])
    _, min_x = min(output, key=lambda p: p[1])

    next_gen = set()
    for y in range(min_y-1, max_y+2):
        for x in range(min_x-1, max_x+2):
            p = (y, x)
            s = 0
            for i, ap in enumerate(around(p)):
                ay, ax = ap
                if min_y <= ay <= max_y and min_x <= ax <= max_x:
                    s |= (ap in output) << (8-i)
                else:
                    s |= outside << (8-i)

            if algorithm[s]:
                next_gen.add(p)

    output = next_gen
    outside = not outside

print(len(output))
