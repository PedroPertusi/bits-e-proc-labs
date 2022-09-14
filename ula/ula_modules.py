#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b #xor = ^ #(not a and b) or (a and not b)
        carry.next = a & b #and = &, or = | #(a and b)

    return instances()

# @block
# def fullAdder(a, b, c, soma, carry):
#     s = [Signal(bool(0)) for i in range(3)]

#     half_1 = halfAdder(a, b, s[0], s[1]) 
#     half_2 = halfAdder(c, s[0], soma, s[2]) 

#     @always_comb
#     def comb():
#         carry.next = s[1] | s[2]
#     return instances()

@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]  # 


    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()

@block
def adder2bits(x, y, soma, carry):
    c2 = Signal(bool(0))
    h_1 = halfAdder(x[0], y[0], soma[0], c2) 
    h_2 = fullAdder(x[1], y[1], c2, soma[1], carry)
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    faList = [None for _ in range(n)]
    carryList = [Signal(bool(0)) for _ in range(n+1)]
    for i in range(n):
        faList[i] = fullAdder(x[i], y[i], carryList[i], soma[i], carryList[i+1])
    @always_comb
    def comb():
        carry.next = carryList[-1]
    return instances()

@block
def adderModbv(x, y, soma, carry):
    @always_comb
    def comb():
        sum = x + y
        soma.next = sum
        if sum > x.max - 1:
            carry.next = 1
        else:
            carry.next = 0
    return comb
