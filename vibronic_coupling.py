#! /usr/bin/python

import sys
import math
import gc
import numpy
import re
from scipy import linalg

def vibronic_coupling_raw_matrix(record):
    files = open(record,'r').readlines()
    x=[]
    rownumber = len(files)
    for row in files:
        stri = str.split(row)
        for nu in stri[1:]:
            x.append(float(nu))
    matrix = numpy.array(x).reshape(rownumber,3)
    matrix = matrix.T
    return(matrix,rownumber)


def func(line):
    if len(line) == 1 and line[0].isdigit():
        return 2
    if len(line) == 2 and line[0] == 'Freq':
        return 3
    if len(line) == 3 and line[1] == 'masses':
        return 4
    if len(line) == 5 and line[0].isdigit():
        return 11
    return 0

def superimpose_get_name(record):
    files = open(record,'r').readlines()
    pat = re.compile(r'\b(\w{1,2}).*?')
    x = []
    for row in files:
        x.append(pat.match(row).group(1))
    return x
atom = {'C':12.011,'H':1.008}

file_change = sys.argv[1]
file_base = sys.argv[2]
file_freq = sys.argv[3]

matrix_change,rownumber_1 = vibronic_coupling_raw_matrix(file_change)
matrix_base,rownumber_2 = vibronic_coupling_raw_matrix(file_base)

if not rownumber_1 == rownumber_2:
    print('Rownumber is not equal.')
#    exit 0
rownumber = rownumber_2

name = superimpose_get_name(file_base)
mass = [0,]*rownumber
for ni in range(0,rownumber):
    mass[ni] = (atom.get(name[ni]))

delta_matrix = (matrix_change - matrix_base)
#for ni in range(0,rownumber):
#    for nj in range(0,3):
#        delta_matrix[nj,ni] = (mass[ni])*delta_matrix[nj,ni]
delta_matrix = delta_matrix.reshape((1,3*rownumber))

control_matrix = numpy.zeros([210,210])
for ni in range(0,70):
    flag = 0
    if ni < 6:
        flag = 1
    if ni > 7 and ni < 14:
        flag = 1
    if ni > 35 and ni < 40:
        flag =1
    if ni > 61 and ni < 66:
        flag =1
    if flag:
        control_matrix[3*ni,3*ni] = control_matrix[3*ni+1,3*ni+1] = control_matrix[3*ni+2,3*ni+2] = 1
contron_flag = 0
if contron_flag:
    delta_matrix = delta_matrix.dot(control_matrix)

lines_freq = open(file_freq,'r')
count = -1
while True:
    line = lines_freq.readline().split() 
    flag = func(line)
    if not line:
        break
    if  count == -1:
        freq = 0.
        red_mass = 0.
        order = 0
        x_list = []
        count = 0
        gc.collect()
    if(flag):
        if(flag == 2):
            order = int(line[0])
        if(flag == 3):
            freq = float(line[1])
        if(flag == 4):
            red_mass = float(line[2])
        if(flag > 10):
            count += 1
            for ni in line[2:]:
                x_list.append(float(ni))
    alpha = math.sqrt(freq*red_mass)*0.1728935
    if count == rownumber:
        x_matrix = numpy.array(x_list).reshape(rownumber,3).reshape(rownumber*3,1)
        x_del = delta_matrix.dot(x_matrix)
        kapp = x_del*alpha
        kappa = freq*kapp
        print('%d\t%f\t%f\t%e\t%e\t%e\t%e' %(order,freq,red_mass,alpha,x_del,kapp,kappa))
        count = -1
