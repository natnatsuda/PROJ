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


df = pd.read_csv('linkweb.csv')
j = open('dictstoken1.json')
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


def search(search,dicts):
  c = 0
  k = 0
  for i in search: 
    c += 1 
    if i in dicts.keys(): 
      c += 1
      k += 1
    else:
      c = 0
  return k,c


def intersec(search,dicts,c):
  intersect = {}
  n = 0
  for i in search:
    c += 1
    if i in dicts.keys():
      c += 1
      lists = []
      for j in dicts[i]:
        c += 1
        lists.append(j)
        s = set(lists)
      intersect[n] = s
      n += 1
    else:
      c += 1
      n = 0
      break
 
  first = intersect[0]
  for i in intersect.keys():
    c += 1
    s1 = first.intersection(intersect[i])
    first = s1
    s2 = first
  
  return s2,c

def intersec_position(page,dicts,search,index,c):
  w = search[0]
  z = 0
  num = len(search)
  for i in range(1,num):
    c += 1
    word = search[i]
    w1 = dicts[w][page][index]
    if w1+i in dicts[word][page]:
      c += 1
      z+=1
  return z,c
    
  

def searchword(text):
  p = {}
  t = clearfileandtoken(text)
  s,c = search(t,mydict)
  
  if s == 0 or s < len(t) and s > 0 :
    c += 1
  else:
    inter,c = intersec(t,mydict,c)
    n = 0
    if s == len(t) and s == 1:
      c += 1
      for i in inter:
        c += 1
        n += 1
        p[i] = df['url'][int(i)-1]
    elif s == len(t) and s > 1: 
      c += 1
      for i in inter:
        c += 1
        ww = t[0]
        for j in range(0,len(mydict[ww][i])):
          c += 1
          ip,c = intersec_position(i,mydict,t,j,c)
          if ip == len(t)-1:
            c += 1
            p[i] = df['url'][int(i)-1]
            n += 1
          else:
            p[-1] = "Not Found!!!"

      if n == 0:      
        p[-1] = "Not Found!!!"
  return p,c
  


      
      
        