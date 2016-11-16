#! /usr/bin/python

import sys
import gc

def f0(list1,head,column1,column2,column3):
    return

def f3(list1,head,column1,column2,column3):
    head.append(('',))
    column1.append((list1[0],))
    column2.append((list1[1],))
    column3.append((list1[2],))
    return

def f5(list1,head,column1,column2,column3):
    head.append((list1[0],''))
    column1.append((list1[-3],))
    column2.append((list1[-2],))
    column3.append((list1[-1],))
    return

def f6(list1,head,column1,column2,column3):
    head.append(tuple(list1[0:-4]))
    column1.append((list1[-3],))
    column2.append((list1[-2],))
    column3.append((list1[-1],))
    return

def f11(list1,head,column1,column2,column3):
    head.append(tuple(list1[0:2]))
    column1.append(tuple(list1[2:5]))
    column2.append(tuple(list1[5:8]))
    column3.append(tuple(list1[8:11]))
    return

lnum = {0:f0,3:f3,5:f5,6:f6,11:f11}

def func(line,head,column1,column2,column3):
    list1 = line.split()
    length = len(list1)
    lnum.get(length)(list1,head,column1,column2,column3)
    return

def myprint(outputfile,headi,columni):
    for nn in headi:
        outputfile.write('%-8s' %nn)
    for nn in columni:
        outputfile.write('%8s' %nn)
    outputfile.write('\n')


inputfile = open(sys.argv[1],'r',1)
rownumber = 77

output = 'test.txt'
if len(sys.argv) > 2:
    output = sys.argv[2]
outputfile = open(output,'w')

if len(sys.argv) > 3:
    rownumber = int(sys.argv[3])


count = 0
while True:
    if not count:
        head = []
        column1 = []
        column2 = []
        column3 = []
        gc.collect()
    line = inputfile.readline()
    func(line,head,column1,column2,column3)
    count += 1
    if count == rownumber:
        for ni in range(0,rownumber):
            myprint(outputfile,head[ni],column1[ni])
        for ni in range(0,rownumber):
            myprint(outputfile,head[ni],column2[ni])
        for ni in range(0,rownumber):
            myprint(outputfile,head[ni],column3[ni])
        count = 0
    if not line:
        break
outputfile.close()

    
