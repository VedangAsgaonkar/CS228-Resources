#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],

[ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],

[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]

problem3 = [
[ 7, 0, 0,   8, 0, 5,   0, 0, 6],
[ 0, 0, 4,   0, 6, 0,   2, 0, 0],
[ 0, 5, 0,   2, 0, 4,   0, 9, 0],

[ 8, 0, 5,   0, 0, 0,   3, 0, 9],
[ 0, 1, 0,   0, 0, 0,   0, 6, 0],
[ 3, 0, 6,   0, 0, 0,   1, 0, 7],

[ 0, 6, 0,   5, 0, 7,   0, 1, 0],
[ 0, 0, 7,   0, 9, 0,   6, 0, 0],
[ 5, 0, 0,   3, 0, 6,   0, 0, 2]
]

problem = problem3

# define the problem variables
# Hint: three dimentional array
p = [[[ Bool("p_" + str(i) + "_" + str(j) + "_" + str(k)) for k in range(9)] for j in range(9)] for i in range(9)]

def sum_to_one( ls ):
    lst = []
    for i in range(len(ls)-1):
        for j in range(i+1, len(ls)):
            lst.append(Not(And(ls[i], ls[j])))
    lst.append(Or(ls))
    return And(lst)
# Accumulate constraints in the following list 
Fs = []

# Encode already filled positions
for i in range(9):
    for j in range(9):
        if problem[i][j] > 0:
            Fs.append(p[i][j][problem[i][j]-1])


# Encode for i,j  \sum_k x_i_j_k = 1
for i in range(9):
    for j in range(9):
        Fs.append(sum_to_one(p[i][j]))


# Encode for j,k  \sum_i x_i_j_k = 1
for j in range(9):
    for k in range(9):
        Fs.append(sum_to_one([ p[i][j][k] for i in range(9) ]))

# Encode for i,k  \sum_j x_i_j_k = 1
for i in range(9):
    for k in range(9):
        Fs.append(sum_to_one([ p[i][j][k] for j in range(9) ]))

# Encode for i,j,k  \sum_r_s x_3i+r_3j+s_k = 1
for i in range(3):
    for j in range(3):
        for k in range(9):
            Fs.append(sum_to_one([p[3*i+r%3][3*j+r//3][k] for r in range(9) ] ))



s = Solver()
s.add( And( Fs ) )

if s.check() == sat:
    m = s.model()
    for i in range(9):
        if i % 3 == 0 :
            print("|-------|-------|-------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|", end =" ")
            for k in range(9):
                # FILL THE GAP
                # val model for the variables
                # val = m[]
                val = m[Bool("p_" + str(i) + "_" + str(j) + "_" + str(k))]
                if is_true( val ):
                    print("{}".format(k+1), end =" ")
        print("|")
    print("|-------|-------|-------|")
else:
    print("sudoku is unsat")

# print vars
