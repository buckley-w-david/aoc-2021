#!/usr/bin/python

def part_one(lines):
    ones = [0] * len(lines[0])
    zeros  = [0] * len(lines[0])

    for line in lines:
        for i, c in enumerate(line):
            if c == '1':
                ones[i] += 1
            elif c == '0':
                zeros[i] += 1

    gamma = [0] * len(lines[0])
    ep = [0] * len(lines[0])
    for i, zo in enumerate(zip(ones, zeros)):
        o, z = zo
        gamma[i] = '1' if o > z else '0'
        ep[i] = '0' if o > z else '1'

    gamma = int(''.join(gamma), 2)
    ep = int(''.join(ep), 2)
    return gamma*ep

def part_two(lines):
    ogr = lines[:]
    idx = 0
    while len(ogr) != 1:
        ones = 0
        zeros = 0
        for line in ogr:
            if line[idx] == '1':
                ones += 1
            elif line[idx] == '0':
                zeros += 1
        most_common = '1' if ones >= zeros else '0'
        ogr = [l for l in ogr if l[idx] == most_common]
        idx += 1

    co2 = lines[:]
    idx = 0
    while len(co2) != 1:
        ones = 0
        zeros = 0
        for line in co2:
            if line[idx] == '1':
                ones += 1
            elif line[idx] == '0':
                zeros += 1
        least_common = '0' if ones >= zeros else '1'
        co2 = [l for l in co2 if l[idx] == least_common]
        idx += 1

    ogr = int(''.join(ogr), 2)
    co2 = int(''.join(co2), 2)
    return ogr*co2


with open('input') as f:
    lines = [l.strip() for l in f.readlines()]

print(f"Part 1: {part_one(lines)}")
print(f"Part 2: {part_two(lines)}")
