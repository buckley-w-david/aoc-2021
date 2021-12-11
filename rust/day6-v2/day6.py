#!/usr/bin/env python

import numpy as np
from numpy.linalg import matrix_power

"""
Technique I was introduced to by another solution from a co-worker
I worked out the solution after reading https://zobayer.blogspot.com/2010/11/matrix-exponentiation.html

Basically think of modelling the situation as a system of 9 related linear equations

f0(n+1) = f1(n) <- Number of 0s is at generation n+1 is the number of 1s at generation n
f1(n+1) = f2(n)
f2(n+1) = f3(n)
f3(n+1) = f4(n)
f4(n+1) = f5(n)
f5(n+1) = f6(n)
f6(n+1) = f7(n) + f0(n) <- Number of 6s at generation n+1 is the number of 7s + the number of 0s at generation n
f7(n+1) = f8(n)
f8(n+1) = f0(n)


Consider the following state vectors
    ┌       ┐          ┌         ┐
    │ f0(n) │          │ f0(n+1) │  
    │ f1(n) │          │ f1(n+1) │  
    │ f2(n) │          │ f2(n+1) │  
    │ f3(n) │          │ f3(n+1) │  
A = │ f4(n) │      B = │ f4(n+1) │  
    │ f5(n) │          │ f5(n+1) │  
    │ f6(n) │          │ f6(n+1) │  
    │ f7(n) │          │ f7(n+1) │  
    │ f8(n) │          │ f8(n+1) │
    └       ┘          └         ┘

A is our current state, B is the next state.
Given A, we can compute B by multiplying it by M


    ┌                   ┐ 
    │ 0 1 0 0 0 0 0 0 0 │ 
    │ 0 0 1 0 0 0 0 0 0 │ 
    │ 0 0 0 1 0 0 0 0 0 │ 
    │ 0 0 0 0 1 0 0 0 0 │ 
M = │ 0 0 0 0 0 1 0 0 0 │ 
    │ 0 0 0 0 0 0 1 0 0 │ 
    │ 1 0 0 0 0 0 0 1 0 │ 
    │ 0 0 0 0 0 0 0 0 1 │ 
    │ 1 0 0 0 0 0 0 0 0 │ 
    └                   ┘ 

                                     Given the definitions at the top of this explanation
    ┌                   ┐┌       ┐     ┌             ┐   ┌         ┐
    │ 0 1 0 0 0 0 0 0 0 ││ f0(n) │     │    f1(n)    │   │ f0(n+1) │
    │ 0 0 1 0 0 0 0 0 0 ││ f1(n) │     │    f2(n)    │   │ f1(n+1) │
    │ 0 0 0 1 0 0 0 0 0 ││ f2(n) │     │    f3(n)    │   │ f2(n+1) │
    │ 0 0 0 0 1 0 0 0 0 ││ f3(n) │     │    f3(n)    │   │ f3(n+1) │
    │ 0 0 0 0 0 1 0 0 0 ││ f4(n) │  =  │    f4(n)    │ = │ f4(n+1) │
    │ 0 0 0 0 0 0 1 0 0 ││ f5(n) │     │    f5(n)    │   │ f5(n+1) │
    │ 1 0 0 0 0 0 0 1 0 ││ f6(n) │     │ f6(n)+f0(n) │   │ f6(n+1) │
    │ 0 0 0 0 0 0 0 0 1 ││ f7(n) │     │    f7(n)    │   │ f7(n+1) │
    │ 1 0 0 0 0 0 0 0 0 ││ f8(n) │     │    f0(n)    │   │ f8(n+1) │
    └                   ┘└       ┘     └             ┘   └         ┘

Thus, with a given state of each function (how many of each growth state there at a point, which is our input), we can multiply it by M
to calculate the next state

fn(1) = M * fn(0)
fn(2) = M * (M * fn(0))
fn(3) = M * (M * (M * fn(0)))
.
.
.

And given the transitivity of multiplication, we can write this as

fn(k) = M**k * fn(0)

Which gives us a state vector with each growth stage, which we can sum for the total population
"""
M = np.array([
    [0, 1, 0, 0, 0, 0 ,0 ,0 ,0],
    [0, 0, 1, 0, 0, 0 ,0 ,0 ,0],
    [0, 0, 0, 1, 0, 0 ,0 ,0 ,0],
    [0, 0, 0, 0, 1, 0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 1 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,1 ,0 ,0],
    [1, 0, 0, 0, 0, 0 ,0 ,1 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,1],
    [1, 0, 0, 0, 0, 0 ,0 ,0 ,0],
])

A = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])


from aocd import get_data

data = [int(i) for i in get_data(year=2021, day=6).split(",")]
for fish in data:
    A[fish] += 1

generations = 256

print(sum(matrix_power(M, generations) @ A))
