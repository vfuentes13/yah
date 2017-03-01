
class Pricing:
	
	# init method
	def __init__(self, symbol): 
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
		print(query)
		try:
			cur.execute(query)
		except Exception as dbe:
			print('%s -- error selecting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
			conn.rollback()
		stk=pd.DataFrame(cur.fetchall(),columns=["symbol","tradeDate","open_","high_","low_","close_","adjClose","volume"])
		return stk

# ------------------------------------------- #

a=Pricing('A')
a.loadHistory('2010-01-01', '2011-01-01')

# stock analysis to be in this class

# create a function that checks if the data exists in the univers
# have that function in a parent universe class and have this one inherits