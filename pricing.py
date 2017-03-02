
class Pricing:
	
	# init method and getters
	def __init__(self, symbol): # we cannot create a symbol from scratch or we have to see if it exists on the server
		self.symbol=symbol
		tradedate='12-31-2099'
		open_=-1
		high_=-1
		low_=-1
		close_=-1
		adjclose=-1
		volume=-1
	
	def getSymbol(self):
		return self.symbol
	
	# no getters and setters as the data will not be modified here, just retrieved
	def loadHistory(self, startDate='1990-01-01', endDate='2099-12-31'):
		query="select * from pricing where symbol='"+ self.getSymbol() +"' and tradedate between '" + startDate + "' and '" + endDate + "';"		
		try:
			cur.execute(query)
		except Exception as dbe:
			print('%s -- error selecting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
			conn.rollback()
		stk=pd.DataFrame(cur.fetchall(),columns=["symbol","tradeDate","open_","high_","low_","close_","adjClose","volume"])
		return stk
	
	def getDailyReturn(self, startDate='1990-01-01', endDate='2099-12-31'):
		df=self.loadHistory(startDate, endDate)
		df=df.ix[:,[1,6]]
		df.columns=['tradedate','adjClose']
		df=df.assign(daily_change=df.adjClose.pct_change(1))
		return df
	
	def getBeta(self, bhk, startDate='1990-01-01', endDate='2099-12-31'):
		df1=self.getDailyReturn(startDate, endDate)		
		df2=bhk.getDailyReturn(startDate, endDate)		
		df=pd.merge(df1, df2, on='tradedate', how='inner')
		df.columns = ['tradedate', 'idx_close', 'idx_return', 'stock_close', 'stock_return']
		idx_var=np.var(df.idx_return)
		covar=df.idx_return.cov(df.stock_return)
		beta=covar/idx_var
		return beta
	
		
# ------------------------------------------- #

a=Pricing('A')
tmp=a.loadHistory('2010-01-01', '2011-01-01')

bhk=Pricing('%5eGSPC')
stk=Pricing('AAPL')
stk.getBeta(bhk)
