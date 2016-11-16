#! /usr/bin/env python

import re
import os
import sys
import math
import numpy
import copy
from scipy import linalg

from scipy.optimize import leastsq

class Coordinates:

    order = 1
    pnum = numpy.ones(order)
    center = numpy.zeros(order)
    center_axis = numpy.zeros(order)
    coef = numpy.ones(order)

#    for i in range(Coordinates.order):
#        baseaxis[i] = max(Coordinates.center[i] - maxcyclenumber,0)
#    for i in range(Coordinates.order):
#        maxaxis[i] = min(Coordinates.center[i] + maxcyclenumber,Coordinates.pnum[i] - 1)
#    for i in range(Coordinates.order):
#        cyclepnum[i] = maxaxis[i] - baseaxis[i] + 1

    def __init__(self,*x):
        self.axis = numpy.zeros(Coordinates.order)
        #self.number = 0
        if len(x) == 1:
            self.axis = numpy.array(x[0])
        if len(x) == 2:
            self.axis = numpy.array(x[0])
            self.const_n = x[1]

    def repnum(x):
        Coordinates.pnum = numpy.array(x)

    def recenter(*x):
        if len(x) == 1:
            Coordinates.center = numpy.array(x[0])
        if len(x) == 0:
            for i in range(Coordinates.order):
                Coordinates.center[i] = Coordinates.pnum[i]//2
    def recoef(*x):
        if len(x) == 1:
            Coordinates.coef = numpy.array(x[0])
        if len(x) == 0:
            Coordinates.coef = numpy.ones(Coordinates.order)
            for i in range(Coordinates.order):
                for j in Coordinates.pnum[i+1:]:
                    Coordinates.coef[i] *= j

    def cycle(self):
        matrcycle = numpy.zeros(Coordinates.order)
        for i in range(Coordinates.order):
            matrcycle[i] = self.axis[i] - Coordinates.center[i]
        return matrcycle

    def maxcycle(self):
        matrcycle = Coordinates.cycle(self)
        maxcyclenumber = max(abs(matrcycle))
        return maxcyclenumber

    def reorder(x):
        order = x
        pnum = numpy.ones(order)
        center = numpy.ones(order)
        coef = numpy.ones(order)

    def number(self):
        axisnumber = 0
        for i in range(Coordinates.order):
            axisnumber += Coordinates.coef[i] * self.axis[i]
        return int(axisnumber)
    


def formnumbers(maxcyclenumber):
    numbers = []
    cyclepnum = numpy.zeros(Coordinates.order)
    baseaxis = numpy.zeros(Coordinates.order)
    maxaxis = numpy.zeros(Coordinates.order)
    for i in range(Coordinates.order):
        baseaxis[i] = max(Coordinates.center[i] - maxcyclenumber,0)
    for i in range(Coordinates.order):
        maxaxis[i] = min(Coordinates.center[i] + maxcyclenumber,Coordinates.pnum[i] - 1)
    for i in range(Coordinates.order):
        cyclepnum[i] = maxaxis[i] - baseaxis[i] + 1
    for const_n in range(Coordinates.order):
        rang = list(reversed(range(Coordinates.order)))
        rang.remove(const_n)
        for axis_const_n in [0,cyclepnum[const_n]-1]:
            if abs(axis_const_n + baseaxis[const_n] - Coordinates.center[const_n]) != maxcyclenumber:
                continue
            axis = numpy.zeros(Coordinates.order)
            axis[const_n] = axis_const_n
            while True:
                x = Coordinates(axis + baseaxis,const_n)
                #for i in range(Coordinates.order):
                #    x.number += int(Coordinates.coef[i] * axis[i])
                flag = True
                for i in range(const_n + 1,Coordinates.order):
                    if abs(axis[i] + baseaxis[i] - Coordinates.center[i]) == maxcyclenumber:
                        flag = False
                if flag:
                    numbers.append(x)
                #numbers.append(Coordinates(axis + baseaxis,const_n))
                if Coordinates.order == 1:
                    break
                axis[rang[0]] += 1
                flag = False
                for i in range(Coordinates.order-1):
                    if axis[rang[i]] == cyclepnum[rang[i]]:
                        axis[rang[i]] = 0
                        if i != Coordinates.order - 2:
                            axis[rang[i+1]] += 1
                        else:
                            flag = True
                if flag:
                    break
    return numbers


def file2data(file_list):
    data_list = []
    pat = re.compile(r'(\w*?\.data)')
    for ni in file_list:
        if pat.match(ni):
            data_list.append(pat.match(ni).group(1))
    return data_list

def func(p,matr):
    tlk = p
    m,n = matr.shape
    x1 = numpy.zeros(m)
    x2 = numpy.zeros(m)
    result = numpy.zeros(m)
    for i in range(m):
        x1[i] = matr[i,0]
        x2[i] = matr[i,1]
    for i in range(m):
        result[i]= (4.9681+0.003452*x1[i])**2+4*(0.061089*x2[i]+tlk*x1[i]*x2[i])**2
    return result
def error(p,x,y):
    return func(p,x) - y

def str2array(record):
    n = int(record[0])
    #m = record[1]
    m = 3
    files = open(record,'r').readlines()
    x = []
    y = []
    for ni in files:
        stri = ni.split()
        for nj in stri[0:n]:
            x.append(float(nj))
        for nj in stri[n:]:
            y.append(float(nj))
    x = numpy.array(x).reshape(len(x)//n,n)
    y = numpy.array(y).reshape(len(y)//m,m)
    rownumber,n = x.shape
    return (x,y,n,m,rownumber)

def diffdecide(ni,y,m):
    swap = list(y[ni.number()])
    result = []
    if ni.cycle()[ni.const_n] > 0:
        sgn = 1
    else:
        sgn = -1
    diff = [0.]*m
    temp = Coordinates()
    for i in range(m):
        temp = copy.deepcopy(ni)
        temp.axis[temp.const_n] -= sgn
        diff[i] += -2*y[temp.number(),i]
        temp.axis[temp.const_n] -= sgn
        diff[i] += 1*y[temp.number(),i]
        #temp.axis[temp.const_n] -= sgn
        #diff[i] += -3*y[temp.number(),i]
        #temp.axis[temp.const_n] -= sgn
        #diff[i] += 3*y[temp.number(),i]
        #temp.axis[temp.const_n] -= sgn
        #diff[i] += -1*y[temp.number(),i]
    print(diff,ni.number())
    for i in range(m):
        temp = [0] * len(swap)
        for j in range(len(swap)):
            temp[j] = abs(diff[i] + swap[j])
        print(temp)
        print(swap)
        result.append(swap[temp.index(min(temp))])
        swap.remove(result[i])
    return result

def swapenergy(record):
    x, y, n, m, rownumber = str2array(record)
    Coordinates.reorder(n)
    for i in range(n):
        temp = []
        for j in range(rownumber):
            temp.append(x[j,i])
        Coordinates.pnum[i] = len(set(temp))
    Coordinates.recenter()
    Coordinates.recoef()
    result = numpy.zeros((rownumber,m))
    for i in range(int(max(Coordinates.pnum))):
        numbers = formnumbers(i)
        if len(numbers) == 0:
            break
        if i < 3:
            for ni in numbers:
                result[ni.number()] = y[ni.number()]
        else:
            for ni in numbers:
                #result[ni.number()] = y[ni.number()]
                result[ni.number()] = diffdecide(ni,y,m)
    for i in range(rownumber):
        print(x[i],result[i])
    return
    #return result















#file_list = os.listdir()
#data_list = file2data(file_list)
#change_energy(data_list)

