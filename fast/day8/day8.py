#!/usr/bin/env python

from aocd import get_data, submit

data = get_data(year=2021, day=8, block=True)
# data = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

lines = [l for l in data.split("\n")]
final_sum = 0
for line in lines:
    encode = {
        0: None,
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
    }
    signals, digits = line.split(" | ")
    digits = digits.split(" ")
    signals = signals.split(" ")

    remove = []
    for digit in signals:
        l = len(digit)
        if l == 2 :
            encode[1] = set(digit)
            remove.append(digit)
        elif l == 4:
            encode[4] = set(digit)
            remove.append(digit)
        elif l == 3:
            encode[7] = set(digit)
            remove.append(digit)
        elif l == 7:
            encode[8] = set(digit)
            remove.append(digit)

    for d in remove:
        signals.remove(d)

    for three in signals:
        s = set(three)
        if len(three) == 5 and len(s - encode[7]) == 2:
            encode[3] = s
            signals.remove(three)
            break

    for nine in signals:
        s = set(nine)
        if len(nine) == 6 and len(s - encode[3]) == 1:
            encode[9] = s
            signals.remove(nine)
            break

    def f():
        for five in signals:
            for six in signals:
                if len(five) == 5 and len(six) == 6:
                    if len(set(six) - set(five)) == 1:
                        encode[5] = set(five)
                        encode[6] = set(six)
                        signals.remove(five)
                        signals.remove(six)
                        return
    f()
    a = encode[7] - encode[1]
    e = encode[6] - encode[5]
    f = encode[7].intersection(encode[5]) - a
    c = encode[7] - a - f
    for digit in signals:
        s = set(digit)
        if len(s) == 5 and a.intersection(s) and e.intersection(s):
            encode[2] = set(digit)
            break

    b = encode[9] - encode[3]
    d = encode[4] - b - c -f
    g = encode[3] - a - c - d -f

    encode[0] = a.union(b).union(c).union(e).union(f).union(g)
    encode[9] = a.union(b).union(c).union(d).union(f).union(g)
    encode[3] = a.union(c).union(d).union(f).union(g)

    decode = {
        ''.join(sorted(encode[0])): 0, 
        ''.join(sorted(encode[1])): 1, 
        ''.join(sorted(encode[2])): 2, 
        ''.join(sorted(encode[3])): 3, 
        ''.join(sorted(encode[4])): 4, 
        ''.join(sorted(encode[5])): 5, 
        ''.join(sorted(encode[6])): 6, 
        ''.join(sorted(encode[7])): 7, 
        ''.join(sorted(encode[8])): 8, 
        ''.join(sorted(encode[9])): 9, 
    }

    final = []
    for digit in digits:
        s = ''.join(sorted(digit))
        final.append(str(decode[s]))
    final_sum += int(''.join(final))


print(final_sum)
# submit(s)
