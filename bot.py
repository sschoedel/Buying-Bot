from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import xml.etree.ElementTree as ET
import product as PM
tree = ET.parse('siteList.xml')
root = tree.getroot()

wordGroups = {}
URLs = {}

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
	for i in range(len(root[0])):
		name = root[0][i].text
		link = root[1][i].text
		URLs.update({name : link})
	# Populate wordGroups array with different key words
	for i in range(len(root[2])):
		group = root[2][i].tag
		# Remove tabs, newlines, and leading and trailing whitespaces
		words = root[2][i].text.split(',')
		for i,word in enumerate(words): 
			words[i] = word.strip()
		wordGroups.update({group:words})

parseXML(root)
# Preprocessing finish

ProductManager = PM.ProductManager(wordGroups, URLs)


# prod = PM.Product("MicroController", "https://righthere", 42.03, "sparkfun")
# print(prod.name)

# Change location when ported to raspbian
driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\Chrome.exe")

