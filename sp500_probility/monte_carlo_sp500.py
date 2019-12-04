#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd


# Define Variables
input_data = {'mood': {'ann_ret':0.,'ann_vol':0.1224},'alpha': {'ann_ret':0.0594,'ann_vol':0.0147},}
# how many iterations
N = 100000
# how many cases
COUNT = 10
T = 12
YEARS = 30 #30年
overall_result = []
# choose number of runs to simulate
curve_dic = {}
i = 0
for n in range(N):
    result = pd.DataFrame()
    for k in input_data.keys():
        mu = input_data[k]['ann_ret']
        vol = input_data[k]['ann_vol']

        # create list of monthly returns using random normal distribution
        monthly_log_returns = np.random.normal(mu/T, vol/math.sqrt(T), T*YEARS)    
        # print(monthly_log_returns)

        result[k] = monthly_log_returns
    result['price'] = result.sum(axis = 1)


    # 检查未来30年的数据的CAPE中位数是否在[16.32, 24.09]之间
    # 大约有1/4 - 1/5的数据符合这个要求
    # 我们模拟100个数据即可
    CAPE_BASE = 30.54
    PRICE_BASE = 3141.26

    result['PRICE_MOCK'] = np.exp(np.cumsum(result['price'])) * PRICE_BASE 
    result['CAPE_MOCK'] = np.exp(np.cumsum(result['mood'])) * CAPE_BASE

    cape_mean = result['CAPE_MOCK'].mean()

    if cape_mean > 24.09 or cape_mean < 16.32:
        continue

    result.to_csv('sample/sample_%d.csv'%(i),index=False)
    print i
    i = i + 1
    if i >= COUNT:
        break











