#!/usr/bin/env python

# print("\033[2J\033[H") # ]]

from aocd import get_data, submit

from pprint import pprint
from math import floor, ceil
from copy import deepcopy

data = get_data(year=2021, day=18, block=True)

class IntWrapper:
    def __init__(self, i, parent=None):
        self.i = i
        self.parent = parent

    def magnitude(self):
        return self.i

    def __repr__(self):
        return str(self.i)

    def __str__(self):
        return str(self.i)

class Number:
    def __init__(self, left, right, parent = None):
        self.left = left
        self.right = right
        self.parent = parent

    @staticmethod
    def from_list(l):
        left, right = l
        if isinstance(left, list):
            left = Number.from_list(left)
        else:
            left = IntWrapper(left)

        if isinstance(right, list):
            right = Number.from_list(right)
        else:
            right = IntWrapper(right)
        n = Number(left, right)
        left.parent = n
        right.parent = n
        return n

    def inorder(self, level=0):
        if isinstance(self.left, Number):
            yield from self.left.inorder(level+1)
        else:
            yield (level, self.left)

        if isinstance(self.right, Number):
            yield from self.right.inorder(level+1)
        else:
            yield (level, self.right)

    def replace_child(self, new, old):
        if self.left is old:
            self.left = new
            self.left.parent = self
        elif self.right is old:
            self.right = new
            self.right.parent = self
        else:
            raise Exception('Child not found')

    def split(self):
        nodes = [n for n in self.inorder()] 
        for i, n in enumerate(nodes):
            level, node = n
            if isinstance(node, IntWrapper) and node.i >= 10:
                new_node = Number.from_list([floor(node.i / 2), ceil(node.i / 2)])
                node.parent.replace_child(new_node, node)
                return

    def explode(self):
        nodes = [n for n in self.inorder()] 
        for i, n in enumerate(nodes):
            level, left = n
            if level == 4:
                _, right = nodes[i+1]
                if i != 0:
                    _, ll = nodes[i-1]
                    ll.i += left.i
                if i+2 < len(nodes):
                    _, rr = nodes[i+2]
                    rr.i += right.i
                left.parent.parent.replace_child(IntWrapper(0), left.parent)
                return

    def reduce(self, level=1):
        while True:
            for n in self.inorder():
                level, node = n
                assert level < 5

                if level == 4:
                    self.explode()
                    break
            else:
                for n in self.inorder():
                    level, node = n
                    assert level < 5

                    if isinstance(node, IntWrapper) and node.i >= 10:
                        nothing_happened = False
                        self.split()
                        break
                else:
                    break

    def magnitude(self):
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __add__(self, other_number):
        a = deepcopy(self)
        b = deepcopy(other_number)
        n = Number(a, b)
        a.parent = n
        b.parent = n
        n.reduce()
        return n

numbers = [Number.from_list(eval(line)) for line in data.splitlines()]
mm = -1
for a in numbers:
    for b in numbers:
        if a is not b:
            c = a + b
            mm = max(c.magnitude(), mm)
print(mm)

