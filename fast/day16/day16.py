#!/usr/bin/env python

print("\033[2J\033[H") # ]]
print("STARTING")

from more_itertools import chunked, take
from aocd import get_data, submit
from aoc_utils import Grid, Graph

import re

bin = {
    0: "0000",
    1: "0001",
    2: "0010",
    3: "0011",
    4: "0100",
    5: "0101",
    6: "0110",
    7: "0111",
    8: "1000",
    9: "1001",
    10: "1010",
    11: "1011",
    12: "1100",
    13: "1101",
    14: "1110",
    15: "1111",
}

data = get_data(year=2021, day=16, block=True)
# data = """CE00C43D881120""".strip()
data = ''.join([bin[int(c, 16)] for c in data])

def parse_packet(packet):
    read = 0
    vs = ''.join(take(3, packet))
    version = int(vs, 2)
    read += 3
    ts = ''.join(take(3, packet))
    type_ = int(ts, 2)
    read += 3
    if type_ == 4: 
        last = False
        n = []
        for chunk in chunked(packet, 5):
            read += len(chunk)
            last = chunk.pop(0) == '0'
            cs = ''.join(chunk)
            n.append(cs)

            if last:
                break

        nn = int(''.join(n), 2)
        print('literal', nn)
        return read, nn
    else:
        length_type_id = next(packet)
        read += 1
        subpackets = []
        if length_type_id == '0':
            ls = ''.join(take(15, packet))
            length = int(ls, 2)
            read += 15
            sr = 0
            print(f"parsing subpacket by length... {length}")
            while sr < length:
                r, sp = parse_packet(packet)
                subpackets.append(sp)
                read += r
                sr += r
            print(f"done parsing subpacket by length... {length}")
        else:
            ns = ''.join(take(11, packet))
            number = int(ns, 2)
            read += 11
            print(f"parsing subpacket by number... {number}")
            for i in range(number):
                r, sp = parse_packet(packet)
                subpackets.append(sp)
                read += r
            print(f"done parsing subpacket by number... {number}")
        result = 0
        if type_ == 0:
            print("sum", subpackets)
            result = sum(subpackets)
        elif type_ == 1:
            result = 1
            print("product", subpackets)
            for sp in subpackets:
                result *= sp
        elif type_ == 2:
            print("min", subpackets)
            result = min(subpackets)
        elif type_ == 3:
            print("max", subpackets)
            result = max(subpackets)
        elif type_ == 5:
            assert len(subpackets) == 2
            print("gt", subpackets)
            result = 1 if subpackets[0] > subpackets[1] else 0
        elif type_ == 6:
            assert len(subpackets) == 2
            print("lt", subpackets)
            result = 1 if subpackets[0] < subpackets[1] else 0
        elif type_ == 7:
            assert len(subpackets) == 2
            print("eq", subpackets)
            result = 1 if subpackets[0] == subpackets[1] else 0
        print("result", result)
        return read, result

_, res = parse_packet(iter(data))
print(res)
