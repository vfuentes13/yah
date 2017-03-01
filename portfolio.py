class Portfolio:
	
	# init method and getters
	def __init__(self, name):
		self.name=name
		self.stock=[]
		self.quantity=[]
	
	def getName(self):
		return self.name
		
	def getStock(self):
		return self.stock
	
	def getQuantity(self):
		return self.quantity
	
	def getStockQuantity(self):
		return [self.stock, self.quantity]
	
	def getStockQuantityPairs(self):
		res=[]
		for i in range(0, len(x.getStock())):
			tmp=[self.getStock()[i], self.getQuantity()[i]]
			res.append(tmp)
		return res
	
	# is the stock available in the universe?
	def isStockAvailable(self, stock):
		query='select symbol from universe;' # this line was not tested
		try:
			cur.execute(query)
		except:
			print('%s -- error inserting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
			conn.rollback()
		else:
			res=[i[0] for i in cur.fetchall()]
			if(stock in res):
				return 1
			else:
				return -1

	# addStock to the current session
	def addStock(self, stock, quantity):		
		if(self.isStockAvailable(stock)==1):
			pos=self.stockExistsSession(stock)
			if(pos==-1):
				self.stock.append(stock)
				self.quantity.append(quantity)
				return 1
			else:
				self.quantity[pos]=int(self.quantity[pos])+int(quantity)
				return 2
		else:
			print("stock %s does not exist in the universe " % stock)
			return -1
	
	# does the stock already exist in the current session?
	def stockExistsSession(self, stock):
		if(stock in self.getStock()):
			return x.getStock().index(stock)
		else:
			return -1
	
	# does the stock exist in the current database?
	def stockExistsDB(self, stock):
		query="select * from portfolio where symbol ='" + stock + "' and portfolio = '" + self.getName() + "';"
		try:
			cur.execute(query)
		except Exception as dbe:
			print('%s -- error selecting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
			conn.rollback()
		else:
			if(len(cur.fetchall())==0):
				return 0
			else:
				return 1
	
	# save the portfolio in the database based on the sessions data
	def savePortfolio(self): 
		query_insert='insert into portfolio values (%s,%s,%s);'
		query_update='update portfolio set quantity=quantity+%s where symbol=%s and portfolio=%s'
		pname=self.getName()
		for elt in x.getStockQuantityPairs():
			if(self.stockExistsDB(elt[0])):
				tmp=[int(elt[1]), elt[0], pname]
				query=query_update
			else:			
				tmp=[pname, elt[0], elt[1]]
				query=query_insert
			try:
				cur.execute(query, tmp)
				conn.commit()
			except Exception as dbe: 
				print('%s -- error inserting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
				conn.rollback()
		return 0

			
# ---------------------------------------------- #

# some calls to test the functions

x=Portfolio('test')

x.addStock('A','1')
x.addStock('C','14')
x.addStock('GOOG','10')
x.addStock('X5','1')
x.addStock('A','8')

x.stockExistsSession('C')
x.stockExistsSession('sC')

x.getStockQuantity()
x.getStockQuantityPairs()

x.savePortfolio()

