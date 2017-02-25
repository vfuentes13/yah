import pandas as pd
import numpy as np
import yahoo_finance as yh
import psycopg2 as sql
import time
from yahoo_finance import Share
from multiprocessing import Pool

### functions ###

# load the sp500 tickers
def loadSP500():
	with open("D:\Projets\Yah\sptickers.txt", "r") as f:
		sp500tickers = []
		for line in f:
			sp500tickers.append(line.replace('\n',''))
	return sp500tickers

# performances to be looked at
def getShares(sp500tickers):
	pool = Pool()
	nb_ticker=len(sp500tickers)
	universe=list(pool.map(Share, sp500tickers))
	return universe

# need workaround when getting malformed response from server
def insertHistoricalUniverse(universe, startDate, endDate):
	i=0
	stockerr=[]
	query='insert into pricing values (%s,%s,%s,%s,%s,%s,%s,%s);'
	for stock in universe:
		i+=1
		print('%s -- starting stock #%s ' % (time.strftime('%Y-%m-%d %H:%M:%S'), i))
		try:			
			print('%s -- downloading from yahoo finance ' % (time.strftime('%Y-%m-%d %H:%M:%S')))
			tmp=stock.get_historical(startDate, endDate)
			try:
				print('%s -- inserting in the database ' % (time.strftime('%Y-%m-%d %H:%M:%S')))				
				for line in tmp:				
					tmp_list=dictToListValue(line)
					cur.execute(query, tmp_list)
			except Exception as dbe:
				print('%s -- error inserting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
				conn.rollback()
		except Exception as yhe:			
			print('%s -- error downloading from yahoo finance: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), yhe))
			stockerr.append(stock)
	return stockerr


# outputs a list given a dict
def dictToListValue(tmp):
	tmp_arr=[tmp['Symbol'], tmp['Date'], tmp['Open'], tmp['High'], tmp['Low'], tmp['Close'], tmp['Adj_Close'], tmp['Volume']]	
	return tmp_arr	

# naive because of the response malformed from server
# need to use the list of stocks returned by the function
def initialNaiveSeed(universe):	
	insertHistoricalUniverse(universe, '2000-01-01', '2005-12-31')
	conn.commit()
	insertHistoricalUniverse(universe, '2006-01-01', '2010-12-31')
	conn.commit()
	insertHistoricalUniverse(universe, '2011-01-01', '2015-12-31')
	conn.commit()
	insertHistoricalUniverse(universe, '2016-01-01', '2017-02-24')
	conn.commit()	
	return 0

### main ###

# get sp500 tickers list
sp500tickers=loadSP500()
universe=getShares(sp500tickers[1:])

# connect to the database
conn = sql.connect("dbname='yah' user='usr' password='pwd'")
cur = conn.cursor()

# run the initial seed
initialNaiveSeed(universe)

# close the connection
cur.close()
conn.close()
