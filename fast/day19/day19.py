#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from pprint import pprint
from aocd import get_data, submit
import numpy as np
from numpy.linalg import matrix_power

data = get_data(year=2021, day=19, block=True)
# data = """
# --- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401

# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390

# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562

# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596

# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14
# """.strip()

# Assumption: Distrubtion patterns of beacons are globally unique

class Scanner:
    def __init__(self, points):
        self.points = points

    # I don't know 3d stuff well enough, this is more than 24 permutations
    def point_permutations(self):
        yield {(p[0], p[1], p[2]) for p in self.points}
        yield {(p[0], p[2], p[1]) for p in self.points}
        yield {(p[1], p[0], p[2]) for p in self.points}
        yield {(p[1], p[2], p[0]) for p in self.points}
        yield {(p[2], p[0], p[1]) for p in self.points}
        yield {(p[2], p[1], p[0]) for p in self.points}

        yield {(-p[0], -p[1], -p[2]) for p in self.points}
        yield {(-p[0], -p[2], -p[1]) for p in self.points}
        yield {(-p[1], -p[0], -p[2]) for p in self.points}
        yield {(-p[1], -p[2], -p[0]) for p in self.points}
        yield {(-p[2], -p[0], -p[1]) for p in self.points}
        yield {(-p[2], -p[1], -p[0]) for p in self.points}

        yield {(p[0], -p[1], -p[2]) for p in self.points}
        yield {(p[0], -p[2], -p[1]) for p in self.points}
        yield {(p[1], -p[0], -p[2]) for p in self.points}
        yield {(p[1], -p[2], -p[0]) for p in self.points}
        yield {(p[2], -p[0], -p[1]) for p in self.points}
        yield {(p[2], -p[1], -p[0]) for p in self.points}

        yield {(-p[0], p[1], -p[2]) for p in self.points}
        yield {(-p[0], p[2], -p[1]) for p in self.points}
        yield {(-p[1], p[0], -p[2]) for p in self.points}
        yield {(-p[1], p[2], -p[0]) for p in self.points}
        yield {(-p[2], p[0], -p[1]) for p in self.points}
        yield {(-p[2], p[1], -p[0]) for p in self.points}

        yield {(-p[0], -p[1], p[2]) for p in self.points}
        yield {(-p[0], -p[2], p[1]) for p in self.points}
        yield {(-p[1], -p[0], p[2]) for p in self.points}
        yield {(-p[1], -p[2], p[0]) for p in self.points}
        yield {(-p[2], -p[0], p[1]) for p in self.points}
        yield {(-p[2], -p[1], p[0]) for p in self.points}

        yield {(-p[0], p[1], p[2]) for p in self.points}
        yield {(-p[0], p[2], p[1]) for p in self.points}
        yield {(-p[1], p[0], p[2]) for p in self.points}
        yield {(-p[1], p[2], p[0]) for p in self.points}
        yield {(-p[2], p[0], p[1]) for p in self.points}
        yield {(-p[2], p[1], p[0]) for p in self.points}

        yield {(p[0], -p[1], p[2]) for p in self.points}
        yield {(p[0], -p[2], p[1]) for p in self.points}
        yield {(p[1], -p[0], p[2]) for p in self.points}
        yield {(p[1], -p[2], p[0]) for p in self.points}
        yield {(p[2], -p[0], p[1]) for p in self.points}
        yield {(p[2], -p[1], p[0]) for p in self.points}

        yield {(p[0], p[1], -p[2]) for p in self.points}
        yield {(p[0], p[2], -p[1]) for p in self.points}
        yield {(p[1], p[0], -p[2]) for p in self.points}
        yield {(p[1], p[2], -p[0]) for p in self.points}
        yield {(p[2], p[0], -p[1]) for p in self.points}
        yield {(p[2], p[1], -p[0]) for p in self.points}

    @staticmethod
    def parse(s):
        lines = s.splitlines()
        points = []
        for line in lines[1:]:
            points.append(tuple(map(int, line.split(','))))
        return Scanner(points)

scanners = []
for pl in data.split('\n\n'):
    lines = pl.splitlines()
    points = []
    for line in lines[1:]:
        points.append(tuple(map(int, line.split(','))))
    scanners.append(Scanner(set(points)))

baseline = scanners.pop(0).points

def find_overlapping_coordinates(baseline):
    for scanner in scanners:
        for permutation in scanner.point_permutations():
            for baseline_point in baseline:
                bx, by, bz = baseline_point
                for permutation_point in permutation:
                    px, py, pz = permutation_point
                    x_offset = bx-px
                    y_offset = by-py
                    z_offset = bz-pz

                    matches = 1
                    # As brute force as you can possibly make it...
                    # For every point in every permutation compare it against every point in the set of already known points.
                    # If the offset generated by that permutation point applied to the other points in this permutation give us 12 hits
                    # Then we have a match
                    for mapped_point in permutation:
                        x, y, z = mapped_point
                        if (x+x_offset, y+y_offset, z+z_offset) in baseline:
                            matches += 1
                        if matches >= 12:
                            return scanner, {(x+x_offset, y+y_offset, z+z_offset) for x, y, z in permutation}, (x_offset, y_offset, z_offset)

scanner_positions = [(0, 0, 0)]
while scanners:
    print(len(scanners))
    s, points, offsets = find_overlapping_coordinates(baseline)
    scanner_positions.append(offsets)
    print(points)
    scanners.remove(s)
    baseline.update(points)
print(baseline)
print(len(baseline))
print(scanner_positions)

md = -1
for s1 in scanner_positions:
    a1, b1, c1 = s1
    for s2 in scanner_positions:
        a2, b2, c2 = s2
        md = max(md, (a1-a2)+(b1-b2)+(c1-c2))
print(md)
