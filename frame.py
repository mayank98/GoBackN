class dataframe:
	"""docstring for dataframe"""
	"""length signifies size of the dataframe """
	def __init__(self, length, index, data):
		self.length=length
		self.data=data
		self.index=index

class ackframe:
	"""docstring for ackframe"""
	def __init__(self, length, index):
		self.length=length
		self.index=index