import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
import json
import re


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


def getSectionLinks(url):
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

def getMajorReq(url):
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
    
    reqs = []
    courses = []
    major = []
    print(soup.title.string)
    #use url to get name of course, honours, and before/from 2019
    major.append(re.split("/", url[70:]))
    #major.append(re.findall("\(B[A-z]+.*\s", soup.title.string))
    #major.append(re.findall("in .+,", soup.title.string)[1:])
    for text in soup.strings:
       # print(text + "*****")
        if re.search("[0-9]+\spoints.*", text):
            if len(courses) > 1:
                reqs.append(courses)
            courses = [re.findall("[0-9]+", text)]
            if len(courses) != 1:
                courses = []
        if re.search("[a-z]+.*[A-Z][A-Z][A-Z]*\s[0-9][0-9][0-9].*", text):
            courses.append("Manual entry required")
            courses.append(text)
        elif re.search("[A-Z][A-Z][A-Z]*\s[0-9][0-9][0-9].*", text) != None:
            courses.append(text.split()[:2])
        
    return (major,reqs[1:])



majors = []
url = "https://www.auckland.ac.nz/en/study/study-options/find-a-study-option/bachelor-of-science-bsc.html"
links = getMajorLinks(url)
for link in links:
    for section_link in getSectionLinks(link):
        for section_link_2 in getSectionLinks(section_link):
            print(section_link_2)
            major = getMajorReq(section_link_2)
            majors.append(major)
            print(major)

json_data = json.dumps(majors, indent = 4)
with open("major_reqs.json", "w") as outfile:
    outfile.write(json_data)

            
            




