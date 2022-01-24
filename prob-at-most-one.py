#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time

# number of variables
n=10

# constructed list of variables
vs = [Bool("p"+str(i)) for i in range(n)]

print(vs)

# write function that encodes that exactly one variable is one
def sum_to_one( ls ):
    s = [Bool("s"+str(i)) for i in range(len(ls)-1)]
    base_case = Or(Not(ls[0]), s[0])
    induction_steps = And([ Or( Not(Or(ls[i], s[i-1])), s[i] ) for i in range(1,len(ls)-1) ])
    negation_steps = And([ Or(Not(s[i]), Not(ls[i+1])) for i in range(len(ls)-1) ])
    or_steps = Or(ls)
    return And([base_case, induction_steps, negation_steps, or_steps])

    

# call the function
F = sum_to_one( vs )
print(F)

# construct Z3 solver
solver = Solver()

# add the formula in the solver
solver.add(F)

# check sat value
result = solver.check()

if result == sat:
    # get satisfying model
     m = solver.model()
     print(m)
    # print only if value is true
else:
    print("unsat")
