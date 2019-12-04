#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import numpy as np
import pandas as pd
import datetime
from datetime import datetime, time, timedelta
from dateutil.relativedelta import *
from matplotlib import pyplot as plt
import pymysql
import os.path
from os import path

stock_dict = {}
stocks = []
for line in open('stocks.txt'):
  items = line.strip().split()
  year = str(items[0])
  stock_dict[year] = []
  for item in items[1:]:
    stock_dict[year].append(item)
    if item not in stocks:
      stocks.append(item)


df_lst = []
for code in stocks:
  print '=' * 6, code, '=' * 6
  file = 'stocks/' + code + '.xlsx'
  if not path.exists(file):
    print 'file not exist !!!', file
    exit()
  else:
    df = pd.read_excel(file)
    df = df.set_index('dt')
  df_lst.append(df)
  

df = pd.concat(df_lst, axis=1)
# fill forward
df.fillna(method='ffill')
print df.head()

df = df[df.index > datetime(2006,5 ,1)]

for col in df.columns:
  df[col + '_share'] = 0.0

df['money'] = 0.0
money = 10000.0

target_stocks = []
flag = False # 已处理?
last_idx = None
for idx, row in df.iterrows():
  if idx.month != 5:
    flag = False
  if len(target_stocks) > 0:
    # share不变
    for code in target_stocks:
      df.loc[idx, code + '_share'] = df.loc[last_idx, code + '_share']
    # 计算总值
    money = 0.0
    for code in target_stocks:
      # 有错误先退出
      if df.loc[idx, code] > 0:
        pass
      else:
        print idx, code, df.loc[idx, code]
        exit()
      money += df.loc[idx, code] * df.loc[idx, code + '_share']
  df.loc[idx, 'money'] = money
  # 调仓
  if idx.month == 5 and flag == False: # key dates
    print idx
    year = str(idx.year)
    # 先清空
    for code in target_stocks:
      df.loc[idx, code + '_share'] = 0
    target_stocks = stock_dict[year]
    for code in target_stocks:
      df.loc[idx, code + '_share'] = money / len(target_stocks) / row[code]
    df.loc[idx, 'money'] = money
    flag = True

  last_idx = idx


print df.head(50)
print df.tail(50)