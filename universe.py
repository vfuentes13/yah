
class Universe:
	
	def __init__(self): # we cannot create a symbol from scratch or we have to see if it exists on the server
		symbol=''
		name=''
	
	def symbolExists(self, symbol):
		query="select symbol from universe where symbol = '" + symbol + "';"
		try:
			cur.execute(query)
		except:
			print('%s -- error inserting in the database: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), dbe))
			conn.rollback()
		res=cur.fetchall()
		return res