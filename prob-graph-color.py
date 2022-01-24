#!/usr/bin/python3

from cProfile import label
from z3 import *
import argparse
import itertools
import time
import numpy as np
import matplotlib.pyplot as plt

n = 500
d = 3

# reading edges from a file
# the file has 7000 edges for graph with 500 nodes
edges = []
with open("edges.txt") as f:
    for line in f:
        edges.append([int(v) for v in line.strip().split(',')])


# declare variables 3 color problem for 500 nodes
vs = [ [ Bool ("e_{}_{}".format(i,j)) for j in range(d)] for i in range(n)]

Node_Fs = And([ Or([ vs[i][j] for j in range(d)]) for i in range(n) ])
# encode each nodes has at least one color

# encode neigbouring nodes do not have same color
edge_Fs_list = [ Not(Or( [ vs[edge[0]][j]==vs[edge[1]][j] for j in range(d)] )) for edge in edges ]


# in a loop,
#  -- color nodes after considering only first k edges
#  -- print k,time for solving, sat/unsat
#  -- increase k by delta
# Our aim is to plot k vs. time to solve

# Hint: time.time() returns current time

k     = 10
delta = 10
limit = 2000
sat_arr = []
sat_t = []
unsat_arr = []
unsat_t = []
while k < limit:
    # write the loop body
    edge_Fs = And(edge_Fs_list[:k])
    F = And(Node_Fs, edge_Fs)
    s = Solver()
    t0 = time.time()
    s.add(F)
    result = s.check()
    t1 = time.time()
    t = t1-t0
    if result == sat:
        sat_arr.append(k)
        sat_t.append(t)
    else:
        unsat_arr.append(k)
        unsat_t.append(t)
    k = k + delta

plt.plot(sat_arr, sat_t, label="sat")
plt.plot(unsat_arr, unsat_t, label="unsat")
plt.legend()
plt.show()
