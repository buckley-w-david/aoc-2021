#!/usr/bin/env python

from collections import Counter, defaultdict
from aocd import get_data, submit
import numpy as np
from numpy.linalg import matrix_power

data = get_data(year=2021, day=14, block=True)

template, rules = data.split("\n\n")
rules = dict([tuple(rule.split(" -> ")) for rule in rules.splitlines()])

singles = set(rules.values())
reverse_rules = defaultdict(set)
for single in singles:
    reverse_rules[single].add(single)

for pair, v in set(rules.items()):
    a, b = pair
    reverse_rules[a+v].add(pair)
    reverse_rules[v+b].add(pair)
    reverse_rules[v].add(pair)

fn = {a: b for a, b in rules}

column_index = {k: i for i, k in enumerate(sorted(set(rules.keys()).union(set(rules.values()))))}

f0 = [0 for _ in column_index]

for char in template:
    f0[column_index[char]] += 1

for pair in zip(template, template[1:]):
    a, b = pair
    f0[column_index[a+b]] += 1

M = np.zeros((len(f0), len(f0)), dtype=np.int64)
for col_key, idx_col in column_index.items():
    for row_key, idx_row in column_index.items():
        if row_key in reverse_rules[col_key]:
            M[idx_col, idx_row] = 1

A = np.array(f0)

generations = 40
fg = matrix_power(M, generations) @ A

single_idx = [column_index[s] for s in singles]
single_counts = fg[single_idx]
print(max(single_counts) - min(single_counts))
