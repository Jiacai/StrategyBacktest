#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd


vol_dict = {}
for line in open('vol.txt'):
	line = line.strip()
	items = line.split()
	code = items[0]
	year = str(items[1])
	vol = float(items[2])
	if year not in vol_dict:
		vol_dict[year] = {}
	vol_dict[year][code] = vol

def choose_stock(year):
	year = str(year)
	file_name = 'data/' + year + '.csv'
	stock_dict = {}
	stocks = []
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
			# 排除净值不够一年者
			if code not in vol_dict[year]:
				continue

			stock_dict[code] = items[2]
			roe_lst = [float(items[4]), float(items[5]), float(items[6]), float(items[7]), float(items[8])]
			roe_mean = 1.0
			# roe_lst2 = []
			for roe in roe_lst:
				# roe_lst2.append(1 + roe / 100.0)
				roe_mean *= (1 + roe / 100.0)
			roe_mean = np.power(roe_mean, 1 / 5.0) - 1
			roe_std = np.std(roe_lst)
			pe = float(items[9])
			pb = float(items[10])
			# # Debt to Equity(D/E)
			# d2e = float(items[10])
			stocks.append([code, stock_dict[code], roe_mean, roe_std, pe, pb])

	df = pd.DataFrame(stocks)
	df.columns = ['code', 'name', 'roe_mean', 'roe_std', 'pe', 'pb']

	df['vol'] = float('nan')
	for idx, row in df.iterrows():
		code = row['code']
		if code in vol_dict[year]:
			df.loc[idx, 'vol'] = vol_dict[year][code]

	for col in ['roe_mean', 'roe_std', 'pe', 'pb', 'vol']:
	    col_zscore = col + '_z'
	    df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)

	df['score'] = df['roe_mean_z'] - df['roe_std_z'] - (df['pe_z'] * 2 + df['pb_z']) / 6.0 - df['vol_z'] * 1.5

	df.sort_values(by=['score'], inplace=True, ascending=False)
	# headdf = df.head(30)
	# for idx, row in headdf.iterrows():
	# 	print row['code'], row['name']
	return df.head(50)

# 退市股票，为了回测，过滤
del_lst = ['000022.SZ']

year = 2006

while year <= 2019:
	df = choose_stock(year)
	cnt = 0
	print year,
	for idx, row in df.iterrows():
		if row['code'] not in del_lst:
			print row['code'],
			cnt += 1
		if cnt >= 30:
			break
	print ''
	year += 1

# #打印名字
# while year <= 2019:
# 	df = choose_stock(year)
# 	cnt = 0
# 	print '=' * 10, year, '=' * 10
# 	for idx, row in df.iterrows():
# 		if row['code'] not in del_lst:
# 			print row['code'], row['name']
# 			cnt += 1
# 		if cnt >= 30:
# 			break
# 	print '=' * 10
# 	year += 1