import requests 
import pandas as pd                          
import io
import re
import nltk
import json
import fnmatch

from lxml import html                        
from bs4 import BeautifulSoup                      
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

j = open('dictInverted.json')
mydict = json.load(j)
j.close()

t = []

def clearfileandtoken(content):
  lst = []
  tokens = re.findall("[a-zA-Z*]+",content.lower())
  stopW = set(stopwords.words('english'))
  for w in tokens:
    if w not in stopW: 
      lst.append(w)
  return lst

def listword(text):
    global t
    t = clearfileandtoken(text)
    w = []
    for i in t:
      if i.count('*') != 0:
        fil = fnmatch.filter(mydict.keys(),i)
        for f in fil:
          w.append(f)
    return w



