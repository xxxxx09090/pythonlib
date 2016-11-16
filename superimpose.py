#! /usr/bin/python

import re
import sys
import numpy
import math
from scipy import linalg

def superimpose_get_coordinate(record,m):
    files = open(record,'r').readlines()
    x = []
    n = len(files) 
    for row in files:
        stri = str.split(row)
        for nu in stri[1:m+1]:
            x.append(float(nu))
    matrix = numpy.array(x).reshape(n,m)
    matrix = matrix.T
    return(matrix,n)

def superimpose_get_name(record):
    files = open(record,'r').readlines()
    pat = re.compile(r'\b(\w{1,2}).*?')
    x = []
    for row in files:
        x.append(pat.match(row).group(1))
    return x

def superimpose_move_center(matrix,n,m):
    center = numpy.mean(matrix,axis=1).reshape(m,1)
    res = matrix - numpy.tile(center,numpy.tile(n,1))
    return(res,center)

record_change = sys.argv[1]
record_base = sys.argv[2]

column = 3
if len(sys.argv) > 3:
    column = int(sys.argv[3])

raw_change,rownumber_1 = superimpose_get_coordinate(record_change,column)
raw_base,rownumber_2 = superimpose_get_coordinate(record_base,column)
if not rownumber_1 == rownumber_2 :
    print('Rownumber_1 is not equal rownumber_2.\n')

name = superimpose_get_name(record_base)

matr_change,t_change = superimpose_move_center(raw_change,rownumber_2,column)
matr_base,t_base = superimpose_move_center(raw_base,rownumber_2,column)

print(matr_change.dot(matr_change.T))
inv_change = matr_change.T.dot(linalg.inv(matr_change.dot(matr_change.T)))
r_full = matr_base.dot(inv_change)
u,s,vt = linalg.svd(r_full)
r_rot = u.dot(vt)
res = r_rot.dot(matr_change)
res_t = res+numpy.tile(t_base,(1,rownumber_2))
err = (raw_base - res_t).T

for i_n in range(0,rownumber_2):
    print('%s' %name[i_n],end='')
    for j_n in range(0,column):
        print('\t%9f' %res_t[j_n,i_n],end='')
    print('')
