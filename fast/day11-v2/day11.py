#!/usr/bin/env python

from aocd import get_data, submit
from aoc_utils import Grid

data = get_data(year=2021, day=11, block=True)
# data = """
# 5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526
# """.strip()

class Oct:
    def __init__(self, n):
        self.n = n
        self.flashed = False
        self.flash_count = 0

    def bump(self):
        self.n += 1

    def emit(self):
        if self.n > 9 and not self.flashed:
            self.flash_count += 1
            self.flashed = True
            return True
        return False

    def reset(self):
        if self.n > 9:
            self.n = 0
        self.flashed = False

    def __repr__(self):
        return str(self.n)

    def __str__(self):
        return str(self.n)

lines = [[Oct(int(c)) for c in l] for l in data.split("\n")]
grid = Grid(lines)

def process_flash(y, x):
    for ((y, x), oct) in grid.around_with_index(y, x):
        oct.bump()
        if oct.emit():
            process_flash(y, x)

gen = 0
all_flashed = False
while not all_flashed:
    gen += 1
    grid.apply(Oct.bump)

    for ((y, x), oct) in grid.row_major_with_index():
        if oct.emit():
            process_flash(y, x)

    all_flashed = all([oct.flashed for oct in grid.row_major()])
    grid.apply(Oct.reset)

print(gen)
