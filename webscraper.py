
import urllib.request as urlrq
import certifi
import ssl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
from bs4 import BeautifulSoup
import json

response = urlrq.urlopen("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-science/computer-science.html", context=ssl.create_default_context(cafile=certifi.where()))
html_doc = response.read()
soup = BeautifulSoup(html_doc, 'html.parser')
strhtm = soup.prettify()


course_info = []
courses = soup.find_all("div", class_="coursePaper section")
for course in courses:
    code = course.find("div", class_="courseA").text.strip()
    title = course.find("div", class_="points").text.strip()
    descrition = course.find("p", class_="description").text.strip()

    pre_reqs = [x.text.strip() for x in course.find_all("p", class_="prerequisite")]

    course_info.append([code, title,descrition,pre_reqs])

json_object = json.dumps(course_info, indent=4)
with open("course_information(CS).json", "w") as outfile:
    outfile.write(json_object)