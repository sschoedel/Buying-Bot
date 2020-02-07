from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import xml.etree.ElementTree as ET
import product as PM
import urllib.request
from enum import Enum

searchWords = {}
allWords = []
URLs = {}
searchPrefixes = []
searchSuffixes = []

tree = ET.parse('siteList.xml')
root = tree.getroot()

class XMLtitles(Enum):
	siteName = 0
	searchPrefix = 1
	searchSuffix = 2
	searchWords = 3

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
	# Turn URLs into dict
	for i in range(len(root[XMLtitles.siteName.value])):
		name = root[XMLtitles.siteName.value][i].text
		link = root[XMLtitles.siteLink.value][i].text
		URLs.update({name : link})

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
ProductManager = PM.ProductManager(searchWords, URLs)
# ProductManager.addProduct('name', 'link', 'price', 'website', allWords, discoveredWords)

# for searchTerm in searchTerms:
for i in range(len(URLs)):

# TODO: Change location when ported to raspbian
# Instantiate webdriver
driver = webdriver.Chrome("C:\\Program Files (x86)\\webdrivers\\chromedriver.exe")

def scrape_ebay():
	searchTerm = 'grapes' # TODO: remove this line when implementing different searchterms
	searchTerm = '+'.join(searchTerm.split()) # put plus between each space in search term
	linkPrefix = searchPrefixes[0] # ebay pre/suffix
	linkSuffix = searchSuffixes[0]
	driverSearch = linkPrefix + searchTerm + linkSuffix
	driver.get(driverSearch)
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
	for usageBox in soup.find_all('span', attrs={'class':'SECONDARY_INFO'}):
		usage = usageBox.text
		usages.append(usage)
	for i,shippingBox in enumerate(soup.find_all('span', attrs={'class':'s-item__shipping'})):
		shipping = shippingBox.text
		shippingWords = shipping.split()
		if shippingWords[0].lower() == 'free':
			shipping_price = '0'
		else:
			shipping_price = shippingWords[0].strip('+$')
		shipping_prices.append(shipping_price)
		total_prices.append(float(shipping_price)+float(base_prices[i]))
	# Round total_prices to 2 decmial places and add $
	total_prices = ['%.2f' % float(price) for price in total_prices]
	total_prices = ['$' + str(price) for price in total_prices]

	print(f'imageLinks: {imageLinks}\n links: {links}\n titles: {titles}\n usages: {usages}\n base_prices: {base_prices}\n shipping_prices: {shipping_prices}\n total_prices: {total_prices}')


def scrapeAmazon():
	searchTerm = 'grapes' # TODO: remove this line when implementing different searchterms
	searchTerm = '+'.join(searchTerm.split()) # put plus between each space in search term
	linkPrefix = searchPrefixes[1] #amazon prefix/suffix
	linkSuffix = searchSuffixes[1]
	driverSearch = linkPrefix + searchTerm + linkSuffix
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

	# Populate image links and title lists and save image names
	images = soup.find_all('img', attrs={'class':'s-image'})
	imageName = "amazon-image-"
	imageNames = []
	for i,image in enumerate(images):
		imageName += str(i)
		imageNames.append(imageName)
		imageName = imageName.strip(str(i))
		src = image['src']
		alt = image['alt']
		imageLinks.append(src)
		titles.append(alt)
		# Save image to images folder
		urllib.request.urlretrieve(str(src), "amazonImages\\" + str(imageNames[i]) + ".jpg")

	# Populate usages, links, base_prices, and shipping_prices
	for linkBox in soup.find_all('a', attrs={'class':'s-item__link'}):
		link = linkBox['href']
		links.append(link)
	for priceBox in soup.find_all('span', attrs={'class':'s-item__price'}):
		price = priceBox.text.split()
		price = price[0].strip('$')
		base_prices.append(price)
	for usageBox in soup.find_all('span', attrs={'class':'SECONDARY_INFO'}):
		usage = usageBox.text
		usages.append(usage)
	for i,shippingBox in enumerate(soup.find_all('span', attrs={'class':'s-item__shipping'})):
		shipping = shippingBox.text
		shippingWords = shipping.split()
		if shippingWords[0].lower() == 'free':
			shipping_price = '0'
		else:
			shipping_price = shippingWords[0].strip('+$')
		shipping_prices.append(shipping_price)
		total_prices.append(float(shipping_price)+float(base_prices[i]))
	# Round total_prices to 2 decmial places and add $
	total_prices = ['%.2f' % float(price) for price in total_prices]
	total_prices = ['$' + str(price) for price in total_prices]