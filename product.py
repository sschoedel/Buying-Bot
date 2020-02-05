from compareWord import compare
class ProductManager(object):
	# Variables for score determination
	p = 0.3
	wordThreshold = 1-p
	overallThreshold = 0.8

	def __init__(self, wordGroups, URLs):
		self.wordGroups = wordGroups
		self.URLs = URLs
		self.products = []

	def calculateScore(keyWords, discoveredWords, price):
		numWords = len(discoveredWords)	
		score = 0
		# Make sure bot found something
		if numWords > 0:
			# Calculate word component of score
			wordScore = 0
			for word in keyWords:
				if compare(word, discoveredWords):
					wordScore += 100
			if numWords < 4:
				wordScore /= numWords-2
			else:
				wordScore /= numWords
			# TODO: Calculate price component if word part passes, otherwise return score 0
			# Price scoring requires knowledge of average prices for that part
			# Search through all other listings with similar descriptions and 
			# if wordScore >= wordThreshold:
			# 	wordScore -= price
			# 	score = wordScore

		return score

	def addProduct(self, name, link, price, website, keyWords, discoveredWords):
		score = calculateScore(keyWords, discoveredWords, price)
		if score >= overallThreshold:
			product = Product(name, link, price, website, score)
			products.append(product)

	class Product(object):
		def __init__ (self, name, link, price, website):
			self.name = name
			self.link = link
			self.price = price
			self.website = website
			self.score = score

		def info(self):
			return [self.name, self.link, self.price, self.website]