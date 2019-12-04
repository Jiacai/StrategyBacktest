#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.optimize


# 计算MWR年化收益率
# 10000元存2个月，100000元存1个月，最终变成90000元。
# 计算得MWR年化收益率：-89.16%
# cfDict = {'a':10000, 'b':100000, 'c':-90000}
# wDict = {'a':2.0/12.0, 'b':1.0/12.0, 'c':0}
# return -0.89162962
def calMWR(cfDict, tDict):
    def f(r):
        fvLst = []
        for dt in tDict:
            t = tDict[dt]
            cf = cfDict[dt]
            # print(t, cf)
            fvLst.append(cf * np.exp(r * t))
        v = sum(fvLst)
        return v

    guess = 0.01
    x0 = guess
    sol = sp.optimize.root(f, x0, method='lm')
    return sol
