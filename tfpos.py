import requests 
import pandas as pd                          
import io
import re
import nltk
import json
import math

from lxml import html                        
from bs4 import BeautifulSoup                      
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_csv('linkweb.csv')
j = open('dictstoken1.json')
mydict = json.load(j)
j.close()

n = len(df)

def clearfileandtoken(content):
  lst = []
  tokens = re.findall("[a-zA-Z*]+",content.lower())
  stopW = set(stopwords.words('english'))
  for w in tokens:
    if w not in stopW: 
      lst.append(w)
  return lst

def computeIDF(search,mydict,n):
    countdf = 0
    idf = {}
    for i in search:
        for j in mydict[i]:
            countdf += 1
        idf[i] = math.log10(n/countdf)
    return idf

def computeTFIDF(search,mydict,idf):
    tf = {}
    for i in search:
        for k in range(1,101):
            for j in mydict[i]:
                if k == int(j) :
                    if i in tf:
                        tf[i][int(j)] = len(mydict[i][j]) * idf[i]
                    else:
                        tf[i] = int(j)
                        tf[i] = {int(j) : len(mydict[i][j]) * idf[i]}
                    break
                else:
                    if i in tf:
                        tf[i][int(k)] = 0.0
                    else:
                        tf[i] = int(k)
                        tf[i] = {int(k) : 0.0}
            
    return tf

def computeSIM(tfidf,search):
    sim = {}
    c = 0
    for i in range(1,101):
        for j in search:
            c += tfidf[j][i]
        sim[i] = c
        c = 0
    return sim

def searchword(text,pos):
    txt = []
    ret = {}
    tx = []
    t = clearfileandtoken(text)
    tt = ""
    for i in t:
        if i in mydict:
            txt.append(i)
            tt = tt+i+" "
        else:
            tx.append(i)
            
    f = computeIDF(txt,mydict,n)
    itf = computeTFIDF(txt,mydict,f)

    if len(txt) > 1 and (len(tx) == 0 or len(tx) != 0):
        s = computeSIM(itf,txt)
    elif len(txt) == 1 and (len(tx) == 0 or len(tx) != 0):
        s = itf[txt[0]]
    else:
        s = []
    

    if s != []:
        if len(txt) == len(t):
            sortsim = sorted(s.items(), key=lambda kv: kv[1],reverse = True)
            for i in sortsim:
                for j in pos.keys():
                    if i[1] > 0 and i[0] == int(j) :
                        ret[df['url'][i[0]-1]] = i[1]
        else:
            ret["Not Found!!!"] = 0

    else:
        ret["Not Found!!!"] = 0
    return ret,tt

    



