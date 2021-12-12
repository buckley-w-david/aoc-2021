#!/usr/bin/env python

from aocd import get_data, submit

from collections import defaultdict

data = get_data(year=2021, day=12, block=True)
# data = """
# start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end
# """.strip()

graph = defaultdict(set)

for line in data.split("\n"):
    a, b = line.split("-")
    graph[a].add(b)
    graph[b].add(a)


def visit(node, history, a):
    history.append(node)
    s = 0
    for c in graph[node]:
        if c == "start":
            continue
        if c.islower() and c in history and a is None:
            s += visit(c, history.copy(), c)
        elif c.islower() and c in history:
            continue
        elif c == "end":
            s += 1
        else:
            s += visit(c, history.copy(), a)
    return s

print(visit("start", list(), None))
# submit(s)
