import requests 
import pandas as pd                          
import io
import re
import nltk
import json

from lxml import html                        
from bs4 import BeautifulSoup                      
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

j = open('dictInverted.json')
mydict = json.load(j)
j.close()


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
    ret = {}
    a = 0
    for i in search: 
      if i in mydict:
        c += 1 
        for j in mydict[i]:
          c += 1 
          ret[j] = mydict[i][j]
          a += 1
      elif a == 0:
        c += 1 
        ret["Error"] = "\t\tNot Found!!!"
      else:
        c += 1
        ret[""] = ""
    return ret,c

def searchword(text):
    t = clearfileandtoken(text)
    p,c1 = search(t,mydict)
    return p,c1


