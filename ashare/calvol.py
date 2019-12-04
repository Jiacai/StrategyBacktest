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

import numpy as np
import pandas as pd

year = 2005
stocks = []
while year <= 2019:
    file_name = 'data/' + str(year) + '.csv'
    for line in open(file_name):
        line = line.strip()
        if '=' in line:
            items = line.split(',')
            code = items[1]
            code = code[code.find('"') + 1: code.rfind('"')]
            # 排除B股['2', '9']
            if code[0] == '0':
                code = code + '.SZ'
            elif code[0] == '6':
                code = code + '.SH'
            else:
                continue

            if code in stocks:
                continue

            stocks.append(code)
    year += 1


for code in stocks:
    # print '=' * 6, code, '=' * 6
    file = '../wind/stocks/' + code + '.xlsx'
    if path.exists(file):
        df = pd.read_excel(file)
        df = df.set_index('dt')
        year = 2005
        while year <= 2018:
            tmpdf = df[str(year) + '-05-01' : str(year + 1) + '-05-01']
            if len(tmpdf) > 225:
                tmpdf[code] = np.log(tmpdf[code] / tmpdf[code].shift(1))
                vol = np.std(tmpdf[code]) * np.sqrt(250.0)
                print code, year+1, vol
            year += 1










