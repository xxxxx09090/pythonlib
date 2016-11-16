#! /usr/bin/env python

import re
import os
import sys
import math
import numpy
from scipy import linalg

def superimpose_get_coordinate(record,m):
    files = open(record,'r').readlines()
    x = []
    n = len(files)
    for row in files:
        stri = str.split(row)
        for nu in stri[1:]:
            x.append(float(nu))
    #matrix = numpy.array(x)
    matrix = numpy.array(x).reshape(n,m)
    matrix = matrix.T
    return(matrix,n)

def superimpose_get_mode(record):
    files = open(record,'r').readlines()
    x = []
    n = len(files)
    for row in files:
        stri = str.split(row)
        for nu in stri:
            x.append(float(nu))
    matrix = numpy.array(x).reshape(n//3,3)
    matrix = matrix.T
    return matrix

def superimpose_get_name(record):
    files = open(record,'r').readlines()
    pat = re.compile(r'\b(\w{1,2}).*?')
    x = []
    for row in files:
        x.append(pat.match(row).group(1))
    return x

if len(sys.argv) > 3:
    head = sys.argv[1]
    end = sys.argv[2]
    output = sys.argv[3]

if len(sys.argv) == 2:
    head = 'head.txt'
    end = 'end.txt'
    output = sys.argv[1]

if len(sys.argv) == 1:
    head = 'head.txt'
    end = 'end.txt'
    output = 'test.com'

cartxyz, rownumber1 = superimpose_get_coordinate('xyz.dat',3)
namexyz = superimpose_get_name('xyz.dat')
name = superimpose_get_name('xyz.dat')
modexyz = superimpose_get_mode('normmode.dat')

rot_matrix = numpy.array([0.7071,-0.7071,0.,0.7071,0.7071,0.,0.,0.,1.]).reshape(3,3)
cartxyz = rot_matrix.dot(cartxyz)
modexyz = rot_matrix.dot(modexyz)

alpha = 21.0542
Npoints = 13

xa = -6.
d = 1.

for ipoint in range(0,Npoints):
    print('IPoint = ',end='')
    print('%d'%(ipoint+1))
    sys.stdout.flush()
    os.system('cat %s' %head)
    sys.stdout.flush()
    result = cartxyz + ((ipoint*d+xa)/alpha)*modexyz
    for n_row in range(0,rownumber1): 
        print('%s'%name[n_row],end='')
        for n_col in [2,1,0]:
            print('\t%9f' %result[n_col,n_row],end='')
        print('')
        sys.stdout.flush()
    os.system('cat %s' %end)
    sys.stdout.flush()
print('%s'%'{Table,e1*27.2,e2*27.2,e3*27.2}') 















