#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
from subprocess import call

#-------------------------------
# Exercise :
# consider the following state machine with three bits
#   p' = q \/ r
#   q' = ~p /\ r
#   r' = (q == p)
#
# The machine updates value of the above variables according
# to the above update function. Primed variables indicated
# the next value of the bits
#
# 
# Using SAT solver find a cycle of three states of the state machine
#   -- the cycle must have 3 distinct states
#   -- the states may occur in any order
#----------------------------------

p = [Bool("p"+str(i)) for i in range(4)]
q = [Bool("q"+str(i)) for i in range(4)]
r = [Bool("r"+str(i)) for i in range(4)]
transitions = And([ And([ p[i+1] == Or(q[i],r[i]), q[i+1] == And(Not(p[i]),r[i]), r[i+1] == (q[i] == p[i]) ]) for i in range(3)])
check = And( And([Not(And([ p[i] == p[i+1], q[i] == q[i+1], r[i] == r[i+1] ])) for i in range(3)]), And([p[0] == p[3], q[0] == q[3], r[0] == r[3]]) )
solver = Solver()
F = And(transitions, check)
print(F)
solver.add(F)
result = solver.check()
if result == sat:
    print(solver.model())
else :
    print("unsat")



# state machine 

# p = Bool("p")
# q = Bool("q")
# r = Bool("r")

# p_update = Or( q, r )
# q_update = And( Not(p), r )
# r_update = Not( q == p )

# vs  = [p       ,q       ,r       ]
# ups = [p_update,q_update,r_update]



#----------------------------------------
# a few utitilities 


# supply for fresh bools
var_counter = 0
def count():
    global var_counter
    count = var_counter
    var_counter = var_counter +1
    return str(count)

def get_fresh_bool( suff = "" ):
    return Bool( "b_" + count() + "_" + suff )

def get_fresh_vec( vs, suff = "" ):
    n_vs = []
    for v in vs:
        n_vs.append( get_fresh_bool( suff ) )
    return n_vs

# substitutes a vector of variables
def substitute_vars( formula, from_vars, to_vars ):
    f = formula
    for j in range( 0, len(from_vars) ):
        f = substitute( f, (from_vars[j], to_vars[j]) )
    return f

#-----------------------------------


