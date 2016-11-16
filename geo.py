#! /usr/bin/env python

import re
import os
import sys
import math
import numpy
from scipy import linalg

def readfile(inputfile):
    inputfile_matrix = []
    n = len(inputfile)
    for row in inputfile:
        if row[0] != '!':
            x.append(0)
        elif row[1] == '#':
            x.append(3)
        elif row[1] == '!':
            x.append(4)
        else:
            x.append(10)











inputfile_name = sys.argv[1]
inputfile = open(inputfile_name,'r').readlines()
inputfile_matrix = readfile(inputfile)
