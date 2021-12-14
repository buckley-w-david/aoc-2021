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

# column_index is a mapping from characters to index positions in the initial state (f0) and the matrix 
# It doesn't actually matter which goes where, just that it's fixed
column_index = {k: i for i, k in enumerate(set(rules.keys()).union(set(rules.values())))}

# f0 is the initial state of the counts for each single and each pair
f0 = [0 for _ in column_index]

for char in template:
    f0[column_index[char]] += 1

for pair in zip(template, template[1:]):
    a, b = pair
    f0[column_index[a+b]] += 1


"""
Consider the very simple case
ABC

AA -> B
AB -> A
AC -> C
BA -> B
BB -> B
BC -> A
CA -> C
CB -> B
CC -> A

Our state vectors need an entry for each pair, as well as each individual character
Consider the following state vectors (fx(n) = the count of x in generation n)
    ┌        ┐          ┌          ┐
    │ fA(n)  │          │ fA(n+1)  │  
    │ fB(n)  │          │ fB(n+1)  │  
    │ fC(n)  │          │ fC(n+1)  │  
    │ fAA(n) │          │ fAA(n+1) │  
A = │ fAB(n) │      B = │ fAB(n+1) │  
    │ fAC(n) │          │ fAC(n+1) │  
    │ fBA(n) │          │ fBA(n+1) │  
    │ fBB(n) │          │ fBB(n+1) │  
    │ fBC(n) │          │ fBC(n+1) │
    │ fCA(n) │          │ fCA(n+1) │
    │ fCB(n) │          │ fCB(n+1) │
    │ fCC(n) │          │ fCC(n+1) │
    └        ┘          └          ┘

A is our state at generation n, B is our state at generation n+1
We need to find an M such that MxA = B

Start with zero matrix M of the correct dimentions
    ┌                         ┐ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
M = │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │ 
    └                         ┘ 
Due to how matrix multiplication works, each cell in M encodes how the count in generation n+1 depends on counts in generation n.
Each row and column match the given state function from the A vector in the same position.
For example: 
    - The top left corner is the relationship from one generation to the next on the count of A characters with itself.
    - The bottom left corner is the relationship from one generation to the next on the count of CC pairs given the number of A characters.

We can construct M by reversing the rules given to us as input.
AA -> B - The number of Bs, ABs, and BAs grows by the number of AA characters in the previous generation.
Applying this means that the rows for B, AB, and BA all have a 1 in the column for AA.
The same process is done for all rules.

This gives us how the relationship of pairs and singles grow given the counts pairs in the previous generation.
We then need to factor in that the counts of single characters (A, B, and C in our example) do not decrease from generation to generation. 
Only new characters are introduced. This means in the rows for each single character count, we also need a 1 in the row for that single. 
This is the cell on the main diagonal.

This is the final construction of M
    ┌                         ┐ 
    │ 1 0 0 0 1 0 0 0 1 0 0 1 │
    │ 0 1 0 1 0 0 1 1 0 0 1 0 │
    │ 0 0 1 0 0 1 0 0 0 1 0 0 │
    │ 0 0 0 0 1 0 0 0 0 0 0 0 │
    │ 0 0 0 1 1 0 0 0 0 0 0 0 │
M = │ 0 0 0 0 0 1 0 0 1 0 0 1 │
    │ 0 0 0 1 0 0 1 0 1 0 0 0 │
    │ 0 0 0 0 0 0 1 1 0 0 1 0 │
    │ 0 0 0 0 0 0 0 0 0 0 0 0 │
    │ 0 0 0 0 0 0 0 0 0 1 0 1 │
    │ 0 0 0 0 0 0 0 0 0 0 1 0 │
    │ 0 0 0 0 0 1 0 0 0 1 0 0 │ 
    └                         ┘ 

M * A = B

f(k) = the count of each single and pair in generation k
f(1) = M * f(0)
f(2) = M * (M * f(0))
f(3) = M * (M * (M * f(0)))
.
.
.

And given the transitivity of multiplication, we can write this as

f(k) = M**k * f(0)
"""

M = np.zeros((len(f0), len(f0)), dtype=np.int64)
for col_key, idx_col in column_index.items():
    for row_key, idx_row in column_index.items():
        if row_key in reverse_rules[col_key]:
            M[idx_col, idx_row] = 1

A = np.array(f0)

generations = 40
fg = matrix_power(M, generations) @ A

# Then all one has to do is pick out the singles, find the max and min, and subtract them.
single_idx = [column_index[s] for s in singles]
single_counts = fg[single_idx]
print(max(single_counts) - min(single_counts))
