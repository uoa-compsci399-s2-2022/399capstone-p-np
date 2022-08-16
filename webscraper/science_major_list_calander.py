
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
response = urlrq.urlopen("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-science.html", context=ssl.create_default_context(cafile=certifi.where()))
html_doc = response.read()
soup = BeautifulSoup(html_doc, 'html.parser')
strhtm = soup.prettify()


course_info = []

#Extracts all of the different courses as a HTML objects into a list
courses = soup.find_all("div", class_="badge-text")
for course in courses:

    course_info.append([course.find("a").text.strip(), course.find("a")["href"]])

#Writes file to JSON object 
json_object = json.dumps(course_info, indent=4)
with open("all_courses.json", "w") as outfile:
    outfile.write(json_object)