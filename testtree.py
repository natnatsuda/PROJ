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
j = open('dicttree.json')
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

def search(mydict,words):
    global c
    c = 0
    lendic = len(mydict)
    mid = lendic//2
    setmid = ""
    for i,w in enumerate(mydict):
        if i == mid:
            datanode = chdic(mydict,w)
            setmid = w
    r = Node(datanode)
    for i,w in mydict.items():
        array = chdic(mydict,i)
        insert(r,Node(array))
    
    global l 
    l = []
    l1 = []
    for i in words:
        global wf
        wf = i
        c = inorder(r)
    if len(l) == 0:
        l1.append("Not found!!!")
    else:
        for j in l:
    
            for k in j[1]:
                l1.append(df['url'][int(k)-1])
    return l1,c

def searchword(text):
    t = clearfileandtoken(text)
    p,c1 = search(mydict,t)
    return set(p),c1

class Node: 
    def __init__(self,key): 
        self.left = None
        self.right = None
        self.val = key 
  
def insert(root,node): 
      if root is None: 
          root = node 
      else: 
          if root.val < node.val: 
              if root.right is None: 
                  root.right = node 
              else: 
                  insert(root.right, node) 
          else: 
              if root.left is None: 
                  root.left = node 
              else: 
                  insert(root.left, node)

  
def inorder(root):
    global l
    global c
    if root: 
        c += 1
        global wf
        inorder(root.left)
        if root.val[0] == wf:
            l.append(root.val)
        inorder(root.right)
    return c

def chdic(data,word):
  arr = []
  for i,v in data.items():
    if i == word:
      arr.append(i),arr.append(set(v))
  return arr    