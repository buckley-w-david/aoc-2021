#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from aocd import get_data, submit

data = get_data(year=2021, day=24, block=True)

def base_str(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

class ALU:
    def __init__(self, program):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input = iter("")
        self.program = program

    def read(self):
        # return int(next(self.input))
        print(base_str(self.z, 26))
        print('digit: ', end='')
        return int(input())
    
    @staticmethod
    def parse(s):
        return ALU(s.splitlines())

    def inp(self, a):
        value = self.read()
        setattr(self, a, value)

    def add(self, a, b):
        first = getattr(self, a)
        if b.isnumeric() or (b[0] == '-' and b[1:].isnumeric()):
            second = int(b)
        else:
            second = getattr(self, b)
        setattr(self, a, first+second)
        
    def mul(self, a, b):
        first = getattr(self, a)
        if b.isnumeric() or (b[0] == '-' and b[1:].isnumeric()):
            second = int(b)
        else:
            second = getattr(self, b)
        setattr(self, a, first*second)
        
    def div(self, a, b):
        first = getattr(self, a)
        if b.isnumeric() or (b[0] == '-' and b[1:].isnumeric()):
            second = int(b)
        else:
            second = getattr(self, b)
        setattr(self, a, first//second)

    def mod(self, a, b):
        first = getattr(self, a)
        if b.isnumeric() or (b[0] == '-' and b[1:].isnumeric()):
            second = int(b)
        else:
            second = getattr(self, b)
        setattr(self, a, first % second)

    def eql(self, a, b):
        first = getattr(self, a)
        if b.isnumeric() or (b[0] == '-' and b[1:].isnumeric()):
            second = int(b)
        else:
            second = getattr(self, b)
        setattr(self, a, int(first == second))

    def reset(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def dump(self):
        print(self.w)
        print(self.x)
        print(self.y)
        print(self.z)

    def execute(self, input):
        self.input = iter(str(input))
        for instruction in self.program:
            op, *args = instruction.split()
            getattr(self, op)(*args)

alu = ALU.parse(data)
alu.execute(93151411711311)
alu.dump()
