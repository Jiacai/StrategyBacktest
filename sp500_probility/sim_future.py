#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
import time
import math
import datetime
import decimal
import traceback
import random
import pandas as pd
import numpy as np
import json

from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta



def add_position(max_pos, pos_level, current_pos):
    if current_pos < max_pos:
        return min(max_pos, current_pos + pos_level)
    else:
        return current_pos

def del_position(min_pos, pos_level, current_pos):
    if current_pos > min_pos:
        return max(min_pos, current_pos - pos_level)
    else:
        return current_pos

def run(PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0):
    lst = []
    for line in open('data/cape.txt'):
        lst.append(float(line))
    # 1957年来的数据
    lst = lst[:756]
    lst.reverse()

    result_lst = []
    positive_count = 0.0

    # about future
    # for i in range(100):
    # for i in range(31):
    for i in [9]:
        df = pd.read_csv('sample/sample_%d.csv'%(i))

        CAPE_BASE = 30.54
        PRICE_BASE = 3141.26

        df['PRICE_MOCK'] = np.exp(np.cumsum(df['price'])) * PRICE_BASE 
        df['CAPE_MOCK'] = np.exp(np.cumsum(df['mood'])) * CAPE_BASE

        df = df.drop(['alpha', 'mood', 'price'], axis=1)
        df.columns = ['price', 'cape']

        #######

        df['rtn'] = np.log(df['price'] / df['price'].shift(1))
        cape_list = list(lst)

        df['cape_pct'] = 0.0
        df['position'] = 0.0

        position = 0.0
        for idx, row in df.iterrows():
            cape_list.append(row['cape'])
            cape_s = pd.Series(cape_list)
            cape_rank = cape_s.rank() / float(len(cape_s))
            df.loc[idx, 'cape_pct'] = round(cape_rank.iloc[-1], 4)

            pct = df.loc[idx, 'cape_pct']


            if pct >= 0.9:
                position = PC9
            elif pct >= 0.8:
                position = PC8
            elif pct >= 0.7:
                position = PC7
            elif pct >= 0.6:
                position = PC6
            elif pct >= 0.5:
                position = PC5
            elif pct >= 0.4:
                position = PC4
            elif pct >= 0.3:
                position = PC3
            elif pct >= 0.2:
                position = PC2
            elif pct >= 0.1:
                position = PC1
            else:
                position = PC0
          

            # 这个操作的意思实际是每个月再平衡回这个仓位
            # 并没考虑随着涨跌的变化，不过应该不影响大局
            df.loc[idx, 'position'] = position

        df['sratio'] = df['position'].shift(1)
        df['srtn'] = df['sratio'] * df['rtn']
        df['cumrtn'] = np.cumsum(df['srtn'])
        df['close'] = np.exp(np.cumsum(df['srtn']))
        df['original'] = df['price'] / PRICE_BASE
        # std = np.std(df['srtn']) * np.sqrt(12.0)
        origiReturn = df['price'].iloc[-1] / PRICE_BASE
        newReturn = df['close'].iloc[-1]
        # print i, origiReturn, newReturn, newReturn / origiReturn - 1
        result_lst.append(newReturn / origiReturn - 1)

        if newReturn / origiReturn - 1 > 0:
            positive_count = positive_count + 1
    print 'RESULT', np.mean(result_lst), positive_count/len(result_lst), newReturn
    df.to_excel('df.xlsx')
    exit()
    return np.mean(result_lst), positive_count/len(result_lst)


if __name__ == "__main__":
    PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 = 0.2, 0.9, 0.8, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0
    
    # PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 = 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    
    run(PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0)
    exit()

    base_rtn = -0.1
    base_rate = 0.0
    
    # base_rate = 0.0
    j = 0
    MAX_CNT = 7
    fail_cnt = 0
    # 之后使用逐步求精的方式
    while j < 20:
        if fail_cnt >= MAX_CNT:
            # 随机变异1个求种子

            # PC0 = min(random.random() * 1.0, 1.0)
            # PC1 = min(random.random() * 1.0, 1.0)
            # PC2 = min(random.random() * 1.0, 1.0)
            # PC3 = min(random.random() * 1.0, 1.0)
            # PC4 = min(random.random() * 1.0, 1.0)
            # PC5 = min(random.random() * 1.0, 1.0)
            # PC6 = min(random.random() * 1.0, 1.0)
            # PC7 = min(random.random() * 1.0, 1.0)
            # PC8 = min(random.random() * 1.0, 1.0)
            # PC9 = min(random.random() * 1.0, 1.0)

            # print '*' * 10, 'RESEED', '*' * 10
            # print 'PC9-0:', PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0
            # print '*' * 30

            fail_cnt = 0
        elif j == 0:
            _PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0 = \
                PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0
        else:
            _PC9 = round(min(PC9 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC8 = round(min(PC8 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC7 = round(min(PC7 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC6 = round(min(PC6 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC5 = round(min(PC5 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC4 = round(min(PC4 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC3 = round(min(PC3 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC2 = round(min(PC2 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC1 = round(min(PC1 + (random.random() * 0.2 - 0.1), 1.0), 2)
            _PC0 = round(min(PC0 + (random.random() * 0.2 - 0.1), 1.0), 2)
      
        _PC9 = 0.15
        _PC9 = j * 0.05 + 0.0
        _PC5, _PC6, _PC7, _PC8 = 1.0, 1.0, 1.0, 1.0
        _PC0, _PC1, _PC2, _PC3, _PC4 = 1.0, 1.0, 1.0, 1.0, 1.0
        if min([_PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0]) < 0.0:
            continue

        # if _PC9 > 0.5:
        #     continue


        print 'PC9-0:', _PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0
        print 'round', j, ':CURRENT RATE', base_rate, base_rtn


        rtn, rate = run(_PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0)
        if (rate > base_rate) or (rate == base_rate and rtn > base_rtn):
            print '!!!IMPROVED!!!'
            base_rate = rate
            base_rtn = rtn
            fail_cnt = 0
            PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 = _PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0
            if base_rate > 0.4:
                f = open("params.txt", "w")
                ll = [PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0]
                f.write(str(ll))
                f.close()
        elif (rate < base_rate / 2):
            fail_cnt = MAX_CNT
        else:
            fail_cnt += 1
        print '*' * 30
        j += 1