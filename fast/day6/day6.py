#!/usr/bin/env python

from aocd import data, submit

from itertools import groupby
from functools import cache

fish = sorted([int(i) for i in data.split(",")])
groups = { k: list(l) for k, l in groupby(fish) }

# This is a load bearing cache
@cache
def count_after_generation(pop_count, seed, generations):
    if seed >= generations:
        return pop_count

    generations = generations - seed
    population = pop_count

    for gen in range(0, generations, 7):
        population += count_after_generation(pop_count, 8, generations-gen-1)

    return population

s = 0
for k, group in groups.items():
    s += count_after_generation(len(group), k, 256)
print(s)
