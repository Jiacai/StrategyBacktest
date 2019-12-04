#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import numpy as np
import pandas as pd
import datetime

lst = []
for line in open('data/cape.txt'):
# for line in open('data/prices.txt'):
    lst.append(float(line))

# # 1920年来近100年的数据
# lst = lst[:1200]

# 1957年来近63年的数据（扩展到500只）
lst = lst[:756]

# # 1970年来近50年的数据
# lst = lst[:600]

# # 1990年来近30年的数据
# lst = lst[:360]

# data is in reverse order
lst.reverse() 

x = pd.Series(lst)

# vol = np.std(np.log(x / x.shift(1))) * np.sqrt(12.0)

print 'mean', np.mean(lst), 'median', np.median(lst), 'std', np.std(x) 

lst = []
for line in open('data/prices.txt'):
    lst.append(float(line))

# # 1920年来近100年的数据
# lst = lst[:1200]

# 1957年来近63年的数据（扩展到500只）
lst = lst[:756]

# data is in reverse order
lst.reverse() 

y = pd.Series(lst)

x = np.log(x/x.shift(1))
y = np.log(y/y.shift(1))

df = pd.concat([x, y], axis=1)
df.columns = ['cape_rtn', 'prices_rtn']
df['diff'] = df['prices_rtn'] - df['cape_rtn']

vol = np.std(df['diff']) * np.sqrt(12.0)
print vol










