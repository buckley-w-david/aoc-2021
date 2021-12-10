#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2021, day=10, block=True)

lines = [l for l in data.split("\n")]

M = {
    "(": 0,
    "[": 1,
    "{": 2,
    "<": 3,
}

ME = {
    ")": 0,
    "]": 1,
    "}": 2,
    ">": 3,
}

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,

}

CSCORES = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
}

corrupted = []
s = 0
scores = []
for line in lines:
    states = []
    state = -1
    corrupted = False
    bad_char = None
    for char in line:
        if state == -1:
            state = M[char]
        elif char in M:
            states.append(state)
            state = M[char]
        else:
            if state != ME[char]:
                corrupted = True
                if not bad_char:
                    bad_char = char
            else:
                if states:
                    state = states.pop()
                else:
                    state = -1
    if not corrupted:
        states.append(state)
        s = 0
        while states:
            state = states.pop()
            score = CSCORES[state]
            s *= 5
            s += score
        scores.append(s)
        
ss = sorted(scores)
print(ss[len(ss)//2])
