import requests 
import pandas as pd                          
import io
import re
import nltk
import json
import hashlib

from lxml import html                        
from bs4 import BeautifulSoup                      
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


df = pd.read_csv('linkweb.csv')
j = open('dictInverted.json')
mydict = json.load(j)
j.close()


class HashMap:
	def __init__(self):
		self.size = 65119
		self.map = [None] * self.size
		
	def _get_hash(self, key):
		hash = 0
		for char in str(key):
			hash += ord(char)
		return hash % self.size
		
	def add(self, key, value):
		key_hash = self._get_hash(key)
		key_value = [key, value]
		
		if self.map[key_hash] is None:
			self.map[key_hash] = list([key_value])
			return True
		else:
			for pair in self.map[key_hash]:
				if pair[0] == key:
					pair[1] = value
					return True
			self.map[key_hash].append(key_value)
			return True
			
	def get(self, key,c):
		key_hash = self._get_hash(key)
		if self.map[key_hash] is not None:
			for pair in self.map[key_hash]:
				if pair[0] == key:
					c += 1
					return pair[1],c
		return None,c
			
	def delete(self, key):
		key_hash = self._get_hash(key)
		
		if self.map[key_hash] is None:
			return False
		for i in range (0, len(self.map[key_hash])):
			if self.map[key_hash][i][0] == key:
				self.map[key_hash].pop(i)
				return True
		return False
			
	def print(self):
		for item in self.map:
			if item is not None:
				print(str(item))
			


def clearfileandtoken(content):
	lst = []
	tokens = re.findall("[a-zA-Z]+",content.lower())
	stopW = set(stopwords.words('english'))
	for w in tokens:
		if w not in stopW: 
			lst.append(w)
	return lst


def search(search,mydict):
	c = 0
	h = HashMap()
	ret = {}
	a = 0
	for i in mydict:
		h.add(i,mydict[i])

	for i in search: 
		print(i)
		ha,c = h.get(i,c)
		if ha != None:
			for k,v in ha.items():
				ret[int(k)] = v
				a += 1
		
	if a == 0:
		ret["Error"] = "Not Found!!!"
	else:
		ret[""] = ""
	return ret,c

def searchword(text):
	t = clearfileandtoken(text)
	print(t)
	p,c = search(t,mydict)
	return p,c