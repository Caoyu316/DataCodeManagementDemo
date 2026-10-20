# Week 5 starter: ordinary finite real scalars; text is the invalid-input case.
# Other input domains are outside this exercise, not fully validated here.
import math
import warnings

def f(x):
    x + 1

def my_div(numerator, denominator):
    div = numerator / denominator
    return div

# Task 1: make the return explicit, check +1, then change to +2.
# Task 2: add the supplied text guard to my_div.
# Task 3: modify this same my_div for the new zero policy; preserve the text guard.
