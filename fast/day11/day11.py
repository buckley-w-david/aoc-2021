#!/usr/bin/env python

from aocd import get_data, submit

data = get_data(year=2021, day=11, block=True)
data = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

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

def process_flashes(r, o):
    oct = lines[r][o]
    if oct.emit():
        for i in range(-1, 2):
            for j in range(-1, 2):
                if r+i >= 0 and r+i < len(lines) and o+j >= 0 and o+j < len(row) and not (j == 0 and i == 0):
                    ooct = lines[r+i][o+j]
                    ooct.bump()
                    process_flashes(r+i, o+j)

all_flashed = False
gen = 0
while not all_flashed:
    gen += 1
    for row in lines:
        for oct in row:
            oct.bump()

    for r in range(len(lines)):
        row = lines[r]
        for o in range(len(row)):
            process_flashes(r, o)

    all_flashed = all([oct.flashed for row in lines for oct in row])

    for row in lines:
        for oct in row:
            oct.reset()

print(gen)
