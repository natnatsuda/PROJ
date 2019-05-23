from flask import Flask, render_template, request,redirect,url_for
import test
import testinverted
import testhash
import testtree
import tfidf
import searchengine
import positional
import tfpos

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


app = Flask(__name__)
@app.route('/') 
def index ():
  return render_template("index.html")

def clearfileandtoken(content):
  lst = []
  tokens = re.findall("[a-zA-Z*]+",content)
  stopW = set(stopwords.words('english'))
  for w in tokens:
    if w not in stopW: 
      lst.append(w)
  return lst

@app.route('/result', methods =["POST" , "GET"])
def result():
  global words
  if request.method == "POST":
    result = request.args
    words = request.form['text']
    if len(words) != 0:  
      if words.count('*') != 0:
        w = searchengine.listword(words)
        return render_template("wild.html",result1 = w,text = words) 
      else:
        re1,c1 = testinverted.searchword(words)
        re2,c2 = test.searchword(words)
        re3,c3 = testhash.searchword(words)
        r4,c4 = testtree.searchword(words)
        return render_template("result.html",result1 = re1,count1 = c1,result2 = re2,count2 = c2,result3=re3,count3 = c3,text=words,result4 = r4,count4 = c4)
    else:
      return render_template("Index.html")



@app.route('/rankinverted', methods =["POST" , "GET"])
def rankinverted():
  global words
  if request.method == "POST":
    result = request.args
    words = request.form['text']
    re = {}
    re[""] = "Not Found"
    if len(words) != 0:
      if words.count('*') != 0:
        w = searchengine.listword(words)
        return render_template("wild.html",result1 = w,text = words)
      else:
        re1,tt = tfidf.searchword(words)
        return render_template("rankinverted.html",re1 = re1,tt=tt,text=words,len=len(re1))
    else:
      return render_template("Index.html")

@app.route('/rankPositional', methods =["POST" , "GET"])
def rankPositional():
  if request.method == "POST":
    result = request.args
    words = request.form['text']
    re = {}
    re[""] = "Not Found"
    if len(words) != 0:
      if words.count('*') != 0:
        w = searchengine.listword(words)
        return render_template("wild.html",result1 = w,text = words)
      else:
        pos,c = positional.searchword(words)
        repo,ttpo = tfpos.searchword(words,pos)
        return render_template("rankPositional.html",re2 = repo,tt=ttpo,text=words,len=len(repo))
    else:
      return render_template("Index.html")

@app.route('/wild', methods =["POST" , "GET"])
def wild():
  global words
  if request.method == "POST":
    result = request.args
    words = request.form['text']
    re = {}
    re[""] = "Not Found"
    if len(words) != 0:
      w = searchengine.listword(words)
      return render_template("wild.html",result1 = w,text = words)
    else:
      return render_template("Index.html")


@app.route('/wildcard', methods =["POST" , "GET"])
def wildcard():
  if request.method == "POST":
    result = request.args
    wilds = request.form['text']
   
    t = clearfileandtoken(words)
    for i in t:
      if i.count('*') != 0:
        wil = words.replace(i,wilds)
    pos,c = positional.searchword(wil)
    repo,ttpo = tfpos.searchword(wil,pos)
    sim,tt = tfidf.searchword(wil)

    re1,c1 = testinverted.searchword(wil)
    re2,c2 = test.searchword(wil)
    re3,c3 = testhash.searchword(wil)
    r4,c4 = testtree.searchword(wil)
     
    if len(words) != 0:
      w = searchengine.listword(words)    
  return render_template("wildcard.html",re1=sim,re2=repo,result1 = re1,count1 = c1,result2 = re2,count2 = c2,result3=re3,count3 = c3,text=wil,result4 = r4,count4 = c4,re5 =w,tt=tt)
  

if __name__ == "__main__":     
	  app.run(host = "0.0.0.0")

