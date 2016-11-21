#! /usr/bin/env python

import re
import numpy
from mylittletools import *


dict_rank = {'d4h':16}

dict_weight = {'d4h':numpy.array([1,2,1,2,2,1,2,1,2,2])}

dict_sign = {'d4h':['a1g','a2g','b1g','b2g','eg','a1u','a2u','b1u','b2u','eu']}

def get_dict_signature(stri):
    lit = []
    if stri == 'd4h':
            lit.append(numpy.array([1,1,1,1,1,1,1,1,1,1]))
            lit.append(numpy.array([1,1,1,-1,-1,1,1,1,-1,-1])) 
            lit.append(numpy.array([1,-1,1,1,-1,1,-1,1,1,-1])) 
            lit.append(numpy.array([1,-1,1,-1,1,1,-1,1,-1,1])) 
            lit.append(numpy.array([2,0,-2,0,0,2,0,-2,0,0]))
            lit.append(numpy.array([1,1,1,1,1,-1,-1,-1,-1,-1])) 
            lit.append(numpy.array([1,1,1,-1,-1,-1,-1,-1,1,1])) 
            lit.append(numpy.array([1,-1,1,1,-1,-1,1,-1,-1,1])) 
            lit.append(numpy.array([1,-1,1,-1,1,-1,1,-1,1,-1])) 
            lit.append(numpy.array([2,0,-2,0,0,-2,0,2,0,0])) 
    return lit

class Symmetry_vibration_mode:

    def __init__(self,stri):
        self.symbol = stri
        self.rank = dict_rank.get(self.symbol)
        self.weight = dict_weight.get(self.symbol)
        self.sign = dict_sign.get(self.symbol)
        self.signature = get_dict_signature(self.symbol)

    def read_modes(self,lit):
        self.modes = [None] * len(self.sign)
        for ni in lit:
            self.modes[self.sign.index(ni[0]) ] = ni[1:]
        return self.modes

    def count(self,vector):
        count = []
        for ni in self.signature:
            count.append(numpy.sum(vector * ni * self.weight) / self.rank)
        return numpy.int_(count)

    def symm_time(self,str1,str2):
        timeresult = self.signature[self.sign.index(str1)] * self.signature[self.sign.index(str2)]
        result = self.count(timeresult) 
        return result


def read_symm(record):
    files = open(record).readlines()
    for i in range(len(files)):
        files[i] = files[i].lower().strip()
    temp = files + ['#']
    files = []
    for ni in temp:
        if ni[0] != '#':
            files.append(ni)
    symm_v = Symmetry_vibration_mode(files[0])
    state = rm_nullstr(re.split(r',|:|;|\s',files[1]))
    modes = []
    flag = 0
    for i in files[1:]:
        if i == '{':
            flag = 1
            continue
        if i == '}':
            flag = 0
            break
        if flag:
            modes.append(rm_nullstr(re.split(r',|:|;|\s',i)))
    symm_v.read_modes(modes)
    return symm_v, state 


def state_time(symm_v,state):
    result = []
    for ni in state:
        for nj in state[state.index(ni):]:
            temp = []
            for k in range(len(symm_v.sign)):
                if symm_v.symm_time(ni,nj)[k]:
                    temp.append(symm_v.sign[k])
            result.append((state.index(ni),state.index(nj),temp))
    return result

def mode_time(symm_v,result_state_time):
    result = []
    for ni in result_state_time:
        for nj in ni[2]:
            for nk in symm_v.modes:
                if not nk:
                    continue
               # for nl in nk:
               #     if symm_v.symm_time(symm_v.sign[symm_v.modes.index(nk)],nj)[0]:
               #         one_d.append(nl)
                for nl in symm_v.modes[symm_v.modes.index(nk):]:
                    temp_symm_count = symm_v.symm_time(symm_v.sign[symm_v.modes.index(nk)],symm_v.sign[symm_v.modes.index(nl)])
                    temp_symm_lk = []
                    for si in range(len(symm_v.sign)):
                        if temp_symm_count[si]:
                            temp_symm_lk.append(symm_v.sign[si])
                    if not nl:
                        continue
                    for sk in nk:
                        for sl in nl:
                            for slk in temp_symm_lk:
                                if symm_v.symm_time(slk,nj)[0]:
                                    result.append(list((ni,nj,[int(sk),int(sl)])))

    result_1d = []
    for ni in result:
        if str(ni[2][0]) in symm_v.modes[0]:
            result_1d.append(list((ni[0],ni[1],[int(ni[2][1])])))
    result.extend(result_1d)
    
    result_no_repeat = []
    result_s_modes = []
    result_modes = []
    for ni in result:
        ni[2].sort()
        temp = list((ni[0][0],ni[0][1],ni[2]))
        if not (temp in result_s_modes):
            result_no_repeat.append(ni)
            result_s_modes.append(temp)
        if not ni[2] in result_modes:
            result_modes.append(ni[2])

    result_modes.sort()
    for ni in result_modes:
        print(ni)
                    









