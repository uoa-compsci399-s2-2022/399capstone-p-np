
import urllib.request as urlrq
import certifi
import ssl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
from bs4 import BeautifulSoup
import json




#This is required above normal website reading as the SSL certificate has a problem
#Downloads website as HTML and reads it with BeautifulSoup
def downloadinfo(url, name):
    response = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    strhtm = soup.prettify()


    course_info = []

    #Extracts all of the different courses as a HTML objects into a list
    courses = soup.find_all("div", class_="coursePaper section")
    for course in courses:
        code = course.find("div", class_="courseA").text.strip()
        title = course.find("div", class_="points").text.strip()
        descrition = course.find("p", class_="description").text.strip()

        #Uses a loop to find all the pre_reqs as their own list
        pre_reqs = [x.text.strip() for x in course.find_all("p", class_="prerequisite")]

        course_info.append([code, title,descrition,pre_reqs])

    return course_info
    


response = urlrq.urlopen("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-science.html", context=ssl.create_default_context(cafile=certifi.where()))
html_doc = response.read()
soup = BeautifulSoup(html_doc, 'html.parser')
strhtm = soup.prettify()
course_info = []
courses = soup.find_all("div", class_="badge-text")
for course in courses:
    course_info.append([course.find("a").text.strip(), course.find("a")["href"]])


#Writes file to JSON object 
json_object = json.dumps(course_info, indent=4)
with open("all_courses.json", "w") as outfile:
    outfile.write(json_object)

total = 0
all_course_info = {}
for x in course_info:
    papers = downloadinfo(x[1], x[0])
    total += len(papers)
    all_course_info.update({x[0]:papers})
    print("finished: ",x[0] , " ", total , "papers")

json_object = json.dumps(all_course_info, indent=4)
with open("course_information.json", "w") as outfile:
    outfile.write(json_object)