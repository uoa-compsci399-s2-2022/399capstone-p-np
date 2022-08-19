
import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
import json

f = open('course_name_and_IDs.json')
data = json.load(f)
course_names = data[0]
courseID = data[1]


def downloadinfo(url):
    GENEDS = []
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
    strhtm = soup.prettify()


    course_info = []

    #Extracts all of the different courses as a HTML objects into a list
    courses = soup.find("div", class_="table section")
    z = courses.text
    for x in z.split("\n"):
        temp = (x.strip())
        course_PK = temp.split(" ")
        if len(course_PK) == 2:
            if course_PK[0] in course_names and course_PK[1] in courseID:
                GENEDS.append((course_PK[0], course_PK[1]))
        
    return GENEDS

gen_ed_list = []
all_schedules_url = "https://www.auckland.ac.nz/en/study/study-options/undergraduate-study-options/general-education/course-schedules.html"
response = urlrq.urlopen(all_schedules_url, context=ssl.create_default_context(cafile=certifi.where()))
html_doc = response.read()
soup = BeautifulSoup(html_doc, 'html.parser')
schedules = soup.findAll("li", class_="page-listing__item listing-item")
for x in schedules:
    url = x.find("a")['href']
    name = x.find("p", class_="listing-item__heading").text
    gen_ed_list.append((name,url))

for x in gen_ed_list:
    print(x[0])
    print(downloadinfo(x[1]))
    print(" ")



#gen_ed_list.append(("open",downloadinfo("https://www.auckland.ac.nz/en/study/study-options/undergraduate-study-options/general-education/course-schedules/open-schedule.html")))

