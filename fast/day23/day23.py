#!/usr/bin/env python

print("\033[2J\033[H") # ]]

# from math import fabs
# from aocd import get_data, submit
from aoc_utils import Graph
import re

# data = get_data(year=2021, day=23, block=True)
data = """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
""".strip()

# PROD
data = """
#############
#...........#
###D#D#B#A###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#B#C#
  #########
"""

#############
#0123456789A#
###B#D#F#H###
  #C#E#G#I#
  #########

burrow = {
    0: {1},
    1: {2, 0},
    2: {1, 3, 11},
    3: {2, 4},
    4: {3, 5, 13},
    5: {4, 6},
    6: {5, 7, 15},
    7: {6, 8},
    8: {7, 9, 17},
    9: {8, 10},
    10: {9},
    11: {2, 12},
    12: {11, 19},
    13: {4, 14},
    14: {13, 20},
    15: {6, 16},
    16: {15, 21},
    17: {8, 18},
    18: {17, 22},
    19: {12, 23},
    20: {14, 24},
    21: {16, 25},
    22: {18, 26},
    23: {19},
    24: {20},
    25: {21},
    26: {22},
}
illegal_endpoints = frozenset([2, 4, 6, 8])
hallway_endpoints = frozenset([0,1,2,3,4,5,6,7,8,9,10])
room_endpoints = frozenset([11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])
type_rooms = [
    frozenset([11, 12, 19, 23]),
    frozenset([13, 14, 20, 24]),
    frozenset([15, 16, 21, 25]),
    frozenset([17, 18, 22, 26]),
]
room_top = [
    11,
    13,
    15,
    17,
]
room_mid1 = [
    12,
    14,
    16,
    18,
]
room_mid2 = [
    19,
    20,
    21,
    22,
]
room_bottom = [
    23,
    24,
    25,
    26,
]


bg = Graph()
for b, conns in burrow.items():
    for c in conns:
        bg.add_edge(b, c)
path_lengths = [0 for _ in range(27)]
for i in range(27):
    path_lengths[i] = bg.dijkstra(i)

idx_lookup = {
    0: 11,
    1: 13,
    2: 15,
    3: 17,
    4: 12,
    5: 14,
    6: 16,
    7: 18,
    8: 19,
    9: 20,
    10: 21,
    11: 22,
    12: 23,
    13: 24,
    14: 25,
    15: 26,
    16: 27,
}

char_lookup = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}

starting = re.findall(r"\w", data)

#         A    B    C    D
state = [[ ], [ ], [ ], [ ]]
for i, c in enumerate(starting):
    state[char_lookup[c]].append(idx_lookup[i])
state = tuple(map(frozenset, state))


target_state = tuple(type_rooms)
type_costs = (1, 10, 100, 1000)

def done(state):
    return state == target_state

from more_itertools import flatten

try:
    from functools import cache
except ImportError:
    from functools import lru_cache
    cache = lru_cache(None)

@cache
def is_legal(state, type, target, dest):
    occupied_spaces = frozenset(flatten(state))
    their_room = type_rooms[type]
    # Optimization
    # It is illegal for a piece of move out of the bottom of it's own room
    if room_bottom[type] == target:
        return False

    # Optimization
    # It is illegal to move around within a room
    if target in their_room and dest in their_room:
        return False

    # Optimization
    # It is illegal to move into the upper portion of a room if the bottom is available
    if dest == room_top[type] and room_mid1[type] not in occupied_spaces:
        return False
    if dest == room_mid1[type] and room_mid2[type] not in occupied_spaces:
        return False
    if dest == room_mid2[type] and room_bottom[type] not in occupied_spaces:
        return False

    # Optimization
    # It is illegal to move out of a room holding just your type
    if target in their_room:
        invalid = True
        for i in range(len(state)):
            if i != type:
                for a in state[i]:
                    if a in their_room:
                        invalid = False
        if invalid:
            return False

    if state[type] == target_state[type]:
        return False

    # Can't stop outside doors
    if dest in illegal_endpoints:
        return False

    # Hallway dudes must move into rooms
    if target in hallway_endpoints and dest in hallway_endpoints:
        return False

    # Can't move through/onto another occupied space
    for p in path_lengths[target].path_to(dest)[1:]:
        if p in occupied_spaces:
            return False

    if dest in room_endpoints:
        # Can't move into rooms other than yours
        if dest not in their_room:
            return False
        # Can't move into room occupied by other types
        # Each type of Amphipods
        for i, s in enumerate(state):
            # Each individual Amphipods
            for a in s:
                # If it's in their room, and it's not the same type
                if a in their_room and i != type:
                    return False

    return True

infinity = float('inf')

db = [[c for c in l] for l in """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########
""".strip().splitlines()]
display_map = {
    0: (1, 1),
    1: (1, 2),
    2: (1, 3),
    3: (1, 4),
    4: (1, 5),
    5: (1, 6),
    6: (1, 7),
    7: (1, 8),
    8: (1, 9),
    9: (1, 10),
    10: (1, 11),
    11: (2, 3),
    12: (3, 3),
    13: (2, 5),
    14: (3, 5),
    15: (2, 7),
    16: (3, 7),
    17: (2, 9),
    18: (3, 9),
    19: (4, 3),
    20: (4, 5),
    21: (4, 7),
    22: (4, 9),
    23: (5, 3),
    24: (5, 5),
    25: (5, 7),
    26: (5, 9),
}


chars = ['A', 'B', 'C', 'D']

from copy import deepcopy
def display(state):
    buffer = deepcopy(db)
    for i, (a, b, c, d) in enumerate(state):
        j, k = display_map[a]
        buffer[j][k] = chars[i]
        j, k = display_map[b]
        buffer[j][k] = chars[i]
        j, k = display_map[c]
        buffer[j][k] = chars[i]
        j, k = display_map[d]
        buffer[j][k] = chars[i]
    print('\n'.join(''.join(l) for l in buffer))

min_cost = infinity
def step(state, history, parent_cost):
    # display(state)
    # sleep(1)
    if done(state):
        global min_cost
        if parent_cost < min_cost:
            min_cost = parent_cost
            print(parent_cost)
        return parent_cost
    history.add(state)

    for i, a in enumerate(state):
        for b in a:
            for move in range(27):
                ns = state[0:i] + ((state[i] - {b}).union({move}),) + state[i+1:]
                if ns not in history and is_legal(state, i, b, move):
                    this_cost = type_costs[i]*path_lengths[b].distance_to(move)
                    step(ns, history.copy(), parent_cost+this_cost)

first_round = []
history = {state}
for i, a in enumerate(state):
    for b in a:
        for move in range(27):
            ns = state[0:i] + ((state[i] - {b}).union({move}),) + state[i+1:]
            if ns not in history and is_legal(state, i, b, move):
                this_cost = type_costs[i]*path_lengths[b].distance_to(move)
                first_round.append((ns, history.copy(), this_cost))

def step_explode(s):
    step(*s)

from multiprocessing import Pool
with Pool(len(first_round)) as pool:
    pool.map(step_explode, first_round)
print(min_cost)
