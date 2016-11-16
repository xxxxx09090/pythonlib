#! /usr/bin/env python

import re
import os
import sys
import math
import numpy
from scipy import linalg
import getopt

def superimpose_get_coordinate(record,m):
    files = open(record,'r').readlines()
    x = []
    n = len(files)
    for row in files:
        stri = re.split(r',|;|\s',row)
        stri.remove('')
        for nu in stri[1:]:
            x.append(float(nu))
    #matrix = numpy.array(x)
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


def superimpose_get_mode(record,number):
    files = open(record,'r').readlines()
    x = []
    freq = float(files[3*(number-1)])
    mess = float(files[3*(number-1)+1])
    stri = re.split(r',|;|\s|\n',files[3*(number-1)+2])
    stri.remove('')
    n = len(stri)//3
    for nu in stri:
        x.append(float(nu))
    matrix = numpy.array(x).reshape(n,3)
    matrix = matrix.T
    return (matrix, freq, mess)

head = 'head.dat'
end = 'end.dat'
freqchk = 'freqchk.scr'
output = 'output.txt'

number1 = number2 = 0
number_flag = 0
output_flag = 0

if len(sys.argv) == 4:
    output = sys.argv[3]
    number1 = int(sys.argv[1])
    number2 = int(sys.argv[2])
elif len(sys.argv) == 3:
    number1 = int(sys.argv[1])
    output = sys.argv[2]
else:
    sys.exit(1)

if output == 'default' or '0':
    output_flag = 1
if number2:
    number_flag =1

#if len(sys.argv) == 2:
#    head = 'head.txt'
#    end = 'end.txt'
#    output = sys.argv[1]
#
#if len(sys.argv) == 1:
#    head = 'head.txt'
#    end = 'end.txt'
#    output = 'test.com'

cartxyz, rownumber = superimpose_get_coordinate('xyz.dat',3)
namexyz = superimpose_get_name('xyz.dat')


Npoints = 17
xa = -8.
d = 1.

normal_matrix1, freq1, mess1 = superimpose_get_mode(freqchk,number1)
if number_flag:
    normal_matrix2, freq2, mess2 = superimpose_get_mode(freqchk,number2)

#rot_matrix = numpy.array([0.7071,-0.7071,0.,0.7071,0.7071,0.,0.,0.,1.]).reshape(3,3)
#cartxyz = rot_matrix.dot(cartxyz)
#normal_matrix1 = rot_matrix.dot(normal_matrix1)

if output_flag:
    output = str(number_flag+1)
    output += 'q'
    output += str(number1)
    if number_flag:
        output += 'q'
        output += str(number2)
    #output += '.com'
output = 'com/' + output

#alp = 0.5445
alp = 0.1720
alpha1 = alp*math.sqrt(freq1*mess1)
if number_flag:
    alpha2 = alp*math.sqrt(freq2*mess2)

head_text = open(head,'r').read()
end_text = open(end,'r').read()

#output_file = open(output,'w')

if not number_flag:
    for ipoint in range(0,Npoints):
        output_number = str(ipoint)
        while len(output_number) < 4:
            output_number = '0' + output_number
        output_name = output + 'n' + output_number + '.com'
        output_file = open(output_name,'w')
        output_file.write('Point = ')
        output_file.write('%d\n'%(ipoint+1))
        output_file.write(head_text)
        result = cartxyz + ((ipoint*d+xa)/alpha1)*normal_matrix1
        for n_row in range(0,rownumber): 
            output_file.write('%s'%namexyz[n_row])
            for n_col in [0,1,2]:
                output_file.write('\t%9f' %result[n_col,n_row])
            output_file.write('\n')
        output_file.write(end_text)
        output_file.write('ni(Point)=%d\n'%(ipoint+xa))
        output_file.write('{Table,ni,e1*27.2,e2*27.2,e3*27.2}\n') 
        output_file.close()


if number_flag:
    for ipoint in range(0,Npoints):
        for jpoint in range(0,Npoints):
            points = ipoint*Npoints+jpoint
            output_number = str(points)
            while len(output_number) < 4:
                output_number = '0' + output_number
            output_name = output + 'n' + output_number + '.com'
            output_file = open(output_name,'w')
            output_file.write('Point = ')
            output_file.write('%d\n'%(points+1))
            output_file.write(head_text)
            result = cartxyz + ((ipoint*d+xa)/alpha1)*normal_matrix1+((jpoint*d+xa)/alpha2)*normal_matrix2
            for n_row in range(0,rownumber): 
                output_file.write('%s'%namexyz[n_row])
                for n_col in [0,1,2]:
                    output_file.write('\t%9f' %result[n_col,n_row])
                output_file.write('\n')
            output_file.write(end_text)
            output_file.write('ni(Point)=%d\n'%(ipoint+xa))
            output_file.write('nj(Point)=%d\n'%(jpoint+xa))
            output_file.write('{Table,ni,nj,e1*27.2,e2*27.2,e3*27.2}\n') 
            output_file.close()













