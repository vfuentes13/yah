import pandas as pd
import numpy as np
import psycopg2 as sql
import matplotlib.pyplot as plt
from datetime import datetime

## functions

def getBeta(idx, stk, startDate, endDate):
	df=cleanData(idx, stk, startDate, endDate)
	idx_var=np.var(df.idx_return)
	covar=df.idx_return.cov(df.stock_return)
	beta=covar/idx_var
	return beta

def cleanData(idx, stk, startDate, endDate):
	df=pd.merge(idx, stk, on='tradedate', how='inner')
	df.columns = ['tradedate', 'idx_close', 'idx_return', 'stock_close', 'stock_return']
	df=df.iloc[:,[0,2,4]]
	mask = (df['tradedate'] > startDate) & (df['tradedate'] <= endDate)
	df=df.loc[mask]
	return df

def getAdjClose(ticker):
	query = "select tradeDate, adjClose from pricing where symbol='" + ticker + "' order by tradedate;"
	cur.execute(query)
	stk=pd.DataFrame(cur.fetchall(),columns=['tradedate','adjClose'])
	stk=stk.assign(daily_change=stk.adjClose.pct_change(1))
	return stk

## main

# db connection
conn = sql.connect("dbname='yah' user='usr' password='pwd'")
cur = conn.cursor()

sp500=getAdjClose('%5eGSPC')
aapl=getAdjClose('AAPL')
getBeta(aapl, sp500, '2016-01-01', '2017-02-25')

# close the connection
cur.close()
conn.close()





#---------------------------------------------#
#---------------------------------------------#
#---------------------------------------------#

cur.execute('''select tradeDate, symbol, adjClose from pricing order by symbol, tradedate;''')
all_stocks=pd.DataFrame(cur.fetchall(),columns=['tradedate','symbol','adjClose'])

dates=all_stocks.tradedate.unique()
symbols=all_stocks.symbol.unique()

all_stocks_clean=pd.DataFrame(index=dates, columns=symbols)

mask = (merged['tradedate'] > '2016-01-01') & (merged['tradedate'] <= '2017-02-02')
merged.loc[mask]

for stock in symbols: 
	print(stock)
	for date in dates:
		print(date)
		val=all_stocks.loc[(all_stocks.tradedate == date) & (all_stocks.symbol == stock)].adjClose
		all_stocks_clean[stock][date]=val

# get sp500 directly 





#---------------------------------------------#
#-------------------garbage-------------------#
#---------------------------------------------#
np.datetime64(aapl.tradedate).astype(datetime)

def convertDates(dt):
	return np.datetime64(dt).astype(datetime)

x=map(convertDates, aapl.tradedate)

for stock in all_stocks.symbol.unique():
	all_stocks.loc[(all_stocks.symbol == stock)]
	all_stocks2=all_stocks

for stock in ('AAPL', 'GOOG'):
	tmp=all_stocks.loc[(all_stocks.symbol == stock)]
	tmp.tradedate

	for date in dates:
	all_stocks.loc[(all_stocks.tradedate == date)]

all_stocks_clean['2017-02-24':]
all_stocks.loc[(all_stocks.tradedate == '2017-02-24')].adjClose


# aaple

# get tradeDate, adjClose
cur.execute('''select tradeDate, adjClose from pricing where symbol='AAPL' order by tradedate;''')
aapl=pd.DataFrame(cur.fetchall(),columns=['tradedate','adjClose'])

# calculate and add daily return
aapl=aapl.assign(daily_change=aapl.adjClose.pct_change(1))#,monthly_change=aapl.adjClose.pct_change(21),yearly_change=df.adjClose.pct_change(252))

# calculate 3 horizon of return moving average
aapl=aapl.assign(MM10=pd.rolling_mean(aapl.adjClose,10),MM50=pd.rolling_mean(aapl.adjClose,50),MM100=pd.rolling_mean(aapl.adjClose,100),MM250=pd.rolling_mean(aapl.adjClose,250))

# plotting result
aapl.plot()
plt.show()

# merge dfs and use the daily returns
merged=pd.merge(sp500, aapl, on='tradedate', how='inner')
merged.columns = ['tradedate', 'idx_close', 'idx_return', 'stock_close', 'stock_return']
merged=merged.iloc[:,[0,2,4]]

# compute variances and covariances:
idx_var=np.var(merged.idx_return)
covar=merged.idx_return.cov(merged.stock_return)
beta=covar/idx_var