import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
import json


def getMajorLinks(url):
    x = 0
    while x < 10:
        try:
            response = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
            x = 100
        except:
            x += 1
    if x != 100:
        print("read fail on ", url)
        return []
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    links = []
    for link in soup.find(id="section6").findAll('a'):
        if link.get('href')[:69] == "https://www.auckland.ac.nz/en/study/study-options/find-a-study-option":
            print(link.get('href'))
            links.append(link.get('href'))
    
    return links

def getStudyLinks(url):
    x = 0
    while x < 10:
        try:
            response = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
            x = 100
        except:
            x += 1
    if x != 100:
        print("read fail on ", url)
        return []
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    links = []
    for link in soup.findAll(class_="subnav-overlay__links"):
        links.append(link.get('href'))

    return links

    

url = "https://www.auckland.ac.nz/en/study/study-options/find-a-study-option/bachelor-of-science-bsc.html"
links = getMajorLinks(url)
for link in links:
    for study_link in getStudyLinks(link):
        print(study_link)




