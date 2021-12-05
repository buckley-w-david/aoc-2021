#!/usr/bin/python

from collections import Counter

with open('input') as f:
    lines = f.readlines()

points = []

for line in lines:
    first, second = line.split(" -> ")
    x1, y1 = [int(i) for i in first.split(",")]
    x2, y2 = [int(i) for i in second.split(",")]
    if x1 == x2:
        smaller = y1 if y1 < y2 else y2
        for y in range(abs(y2-y1)+1):
            points.append((x1, smaller+y))
    elif y1 == y2:
        smaller = x1 if x1 < x2 else x2
        for x in range(abs(x2-x1)+1):
            points.append((smaller+x, y1))
    else:
        if x2 > x1 and y2 > y1:
            for i in range(abs(x1-x2)+1):
                points.append((x1+i, y1+i))
        if x2 > x1 and y2 < y1:
            for i in range(abs(x1-x2)+1):
                points.append((x1+i, y1-i))
        if x2 < x1 and y2 > y1:
            for i in range(abs(x1-x2)+1):
                points.append((x1-i, y1+i))
        if x2 < x1 and y2 < y1:
            for i in range(abs(x1-x2)+1):
                points.append((x1-i, y1-i))
    
counter = Counter(points)
s = len([key for key, value in counter.items() if value > 1])
print(s)
