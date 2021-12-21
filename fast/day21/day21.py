#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from pprint import pprint
from aocd import get_data, submit
from itertools import cycle

data = get_data(year=2021, day=21, block=True)
# data = """
# Player 1 starting position: 4
# Player 2 starting position: 8
# """.strip()

import re
p1, p2 = data.splitlines()
p1_pos = int(re.search(r"starting position: (\d+)", p1).group(1))
p2_pos = int(re.search(r"starting position: (\d+)", p2).group(1))

from functools import cache

@cache
def game(p1_pos, p2_pos, p1_score, p2_score, turn, die):
    if turn:
        p2_pos = ((p2_pos - 1 + die) % 10) + 1
        p2_score += p2_pos
    else:
        p1_pos = ((p1_pos - 1 + die) % 10) + 1
        p1_score += p1_pos

    if p1_score > 20:
        return ( 1, 0 )
    if p2_score > 20:
        return ( 0, 1 )

    turn = not turn

    w1 = 0
    w2 = 0
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                r = game(p1_pos, p2_pos, p1_score, p2_score, turn, a+b+c)
                w1 += r[0]
                w2 += r[1]
    return (w1, w2)


w1 = 0
w2 = 0
turn = 0
for a in range(1, 4):
    for b in range(1, 4):
        for c in range(1, 4):
            r = game(p1_pos, p2_pos, 0, 0, 0, a+b+c) 
            w1 += r[0]
            w2 += r[1]

print(max(w1, w2))
