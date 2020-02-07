from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import xml.etree.ElementTree as ET
import product as PM
import urllib.request
from enum import Enum

products = []

searchWords = {}
allWords = []
siteNames = []
searchPrefixes = []
searchSuffixes = []

tree = ET.parse('siteList.xml')
root = tree.getroot()

class XMLtitles(Enum):
	siteName = 0
	searchPrefix = 1
	searchSuffix = 2
	searchWords = 3

class siteNameTitles(Enum):
	eBayEnum = 0
	amazonEnum = 1

# Only useful for displaying entire XML
def printXML(root):
	if root:
		for child in root:
			print(child.tag, child.text)
			printStuff(child)
	return


# Preprocessing XML file requires bot restart whenever updating XML
# Manually grab important XML info and sort into usable data
def parseXML(root):
	# Turn siteNames into dict
	for i in range(len(root[XMLtitles.siteName.value])):
		siteName = root[XMLtitles.siteName.value][i].text
		siteNames.append(siteName)

	# Populate search prefix and suffix lists
	for i in range(len(root[XMLtitles.searchPrefix.value])):
		searchPrefixes.append(root[XMLtitles.searchPrefix.value][i].text)
		searchSuffixes.append(root[XMLtitles.searchSuffix.value][i].text)
	# Populate searchWords dict with different key words
	for i in range(len(root[XMLtitles.searchWords.value])):
		group = root[XMLtitles.searchWords.value][i].tag
		# Remove tabs, newlines, and leading and trailing whitespaces
		words = root[XMLtitles.searchWords.value][i].text.split(',')
		for i,word in enumerate(words): 
			words[i] = word.strip()
		searchWords.update({group:words})

	# Make list of all words from dict
	[allWords.append(searchWords[i][n]) for i in searchWords for n in range(len(searchWords[i]))]
	
parseXML(root)
# Preprocessing finish
# Repeat everything after this every once in a while to keep updating sites
# Only send new info

# TODO: use product manager and product classes to store products
# Useful for knowing what products are new when sending updates and for comparing
ProductManager = PM.ProductManager(searchWords, siteNames)
# ProductManager.addProduct('name', 'link', 'price', 'website', allWords, discoveredWords)

# TODO: Change location when ported to raspbian
# Instantiate webdriver
driver = webdriver.Chrome("C:\\Program Files (x86)\\webdrivers\\chromedriver.exe")

def scrape_ebay():
	for searchCategory in searchWords: 
		print(f"searching ebay under {searchCategory}")
		for searchWord in searchWords[searchCategory]:
			print(f"searching ebay for {searchWord}")
			searchWord = '+'.join(searchWord.split()) # put plus between each space in search term
			siteNamePrefix = searchPrefixes[siteNameTitles.eBayEnum.value] # ebay pre/suffix
			siteNameSuffix = searchSuffixes[siteNameTitles.eBayEnum.value]
			driverSearch = siteNamePrefix + searchWord + siteNameSuffix
			driver.get(driverSearch)  # Open page
			content = driver.page_source
			soup = BeautifulSoup(content, features="html.parser")
			# Declare useful information lists
			# this information is reset on every search but will be sent to the product class before
			imageLinks = []
			links = []
			titles = []
			usages = []
			base_prices = []
			shipping_prices = []
			total_prices = []

			# Populate image links and title lists and save image names
			images = soup.find_all('img', attrs={'class':'s-item__image-img'})
			imageName = "eBay-image-"
			imageNames = []
			for i,image in enumerate(images):
				imageName += str(i)
				imageNames.append(imageName)
				imageName = imageName.strip(str(i))
				src = image['src']
				alt = image['alt']
				titles.append(alt)
				imageLinks.append(src)
				# Save image to images folder
				urllib.request.urlretrieve(str(src), "ebayImages\\" + str(imageNames[i]) + ".jpg")
			# Populate usages, links, base_prices, and shipping_prices
			for linkBox in soup.find_all('a', attrs={'class':'s-item__link'}):
				link = linkBox['href']
				links.append(link)
			for priceBox in soup.find_all('span', attrs={'class':'s-item__price'}):
				price = priceBox.text.split()
				price = price[0].strip('$')
				base_prices.append(price)
			# Some products don't have a usage labeled so the scraper misses a product and misaligns the rest of the usages
			# Can make this better by searching through each product individually instead of different parts
			# of each product on the entire page
			# for usageBox in soup.find_all('span', attrs={'class':'SECONDARY_INFO'}): 
			# 	usage = usageBox.text
			# 	usages.append(usage)
			for i,shippingBox in enumerate(soup.find_all('span', attrs={'class':'s-item__shipping'})):
				freight = False
				shipping = shippingBox.text
				shippingWords = shipping.split()
				if shippingWords[0].lower() != '+':
					shipping_price = '0'
				else:
					shipping_price = shippingWords[0].strip('+$')
				# TODO: handle freight or other as strings in total_prices and shipping_prices lists
				# else:
				# 	freight = True
				# if freight:
				# 	shipping_price = 'freight'
				shipping_prices.append(shipping_price)
				total_prices.append(float(shipping_price)+float(base_prices[i]))
			# Round total_prices to 2 decmial places and add $
			total_prices = ['%.2f' % float(price) for price in total_prices]
			total_prices = ['$' + str(price) for price in total_prices]

			print(f'imageLinks: {imageLinks}\n links: {links}\n titles: {titles}\n base_prices: {base_prices}\n shipping_prices: {shipping_prices}\n total_prices: {total_prices}')
			for i in range(len(imageLinks)):
				product = [imageLinks[i], links[i], titles[i], base_prices[i], shipping_prices[i], total_prices[i]]
				products.append(product)


def scrape_amazon():
	for searchCategory in searchWords: 
		print(f"searching amazon under {searchCategory}")
		for searchWord in searchWords[searchCategory]:
			print(f"searching amazon for {searchWord}")
			searchWord = '+'.join(searchWord.split()) # put plus between each space in search term
			linkPrefix = searchPrefixes[siteNameTitles.amazonEnum.value] #amazon prefix/suffix
			siteNameSuffix = searchSuffixes[siteNameTitles.amazonEnum.value]
			driverSearch = linkPrefix + searchWord + siteNameSuffix
			driver.get(driverSearch) # open page with search term
			content = driver.page_source
			soup = BeautifulSoup(content, features="html.parser")
			# Declare useful information lists
			# this information is reset on every search but will be sent to the product class before resetting
			imageLinks = []
			links = []
			titles = []
			usages = []
			base_prices = []
			shipping_prices = []
			total_prices = []

			link = 0
			price = 0
			src = 0
			alt = 0

			# badTemplateMatch = False # Used to determine if given product matches regular template defined for the bot

			# Setting find_all before looping allows the bot to take spans with only one class

			# THIS IS GARBAGE CHANGE IT TO MAKE NEW SOUP AND SEARCH THERE FOR EVERY FOUND PRODUCT
			# Populate image links and title lists and save image names
			images = [imageBoxOrig for imageBoxOrig in soup.find_all('span', attrs={'class':'s-product-image'})]
			imageName = "amazon-image-"
			imageNames = []
			strCounter = 0
			for image in images:
				badTemplateMatch = False
				try:
					src = image['src']
					alt = image['alt']
					# Save image to images folder
				except:
					badTemplateMatch = True
				if not badTemplateMatch:
					imageLinks.append(src)
					titles.append(alt)
					imageName += str(strCounter)
					imageNames.append(imageName)
					imageName = imageName.strip(str(strCounter))
					urllib.request.urlretrieve(str(src), "amazonImages\\" + str(imageNames[strCounter]) + ".jpg")
					strCounter += 1

			# Populate linkss and prices
			linkBoxes = [linkBoxOrig for linkBoxOrig in soup.find_all('a', attrs={'class':'a-link-normal'})]
			for linkBox in linkBoxes:
				badTemplateMatch = False
				try:
					link = linkBox['href']
				except:
					badTemplateMatch = True
				if not badTemplateMatch:
					links.append(link)

			priceBoxes = [priceBoxOrig for priceBoxOrig in soup.find_all('span', attrs={'class':'a-offscreen'}) if len(priceBoxOrig["class"]) == 1]
			for priceBox in priceBoxes:
				badTemplateMatch = False
				try:
					price = priceBox.text.split()
					price = price[0].strip('$')
				except:
					badTemplateMatch = True
				if not badTemplateMatch:
					base_prices.append(price)
					shipping_prices.append(0)
					total_prices.append(price) # amazon rarely has shipping prices so set all shipping prices to 0

			# Round total_prices to 2 decmial places and add $
			total_prices = ['%.2f' % float(price) for price in total_prices]
			total_prices = ['$' + str(price) for price in total_prices]
		 
			print(f'imageLinks: {imageLinks}\n links: {links}\n titles: {titles}\n total_prices: {total_prices}')
			for i in range(len(imageLinks)):
				product = [imageLinks[i], links[i], titles[i], total_prices[i]]
				products.append(product)

scrape_ebay()
scrape_amazon()

print(products)