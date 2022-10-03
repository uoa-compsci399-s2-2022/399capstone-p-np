
import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
import json
import sqlite3


sqliteConnection = sqlite3.connect(r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\library\adapters\399courses.db")
cursor = sqliteConnection.cursor()

cursor.execute("delete from courseScheduleLink where 1 == 1")

a = cursor.execute("select * from course")
course = a.fetchall()
newlist = []
course_names =[]
courseID = []
for x in course:
    course_names.append(x[0])
    courseID.append(x[1])


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
    for y in downloadinfo(x[1]):
        print(x[0], y[0], y[1])
        cursor.execute("insert into courseScheduleLink (scheduleID, subject, courseNumber) values  (?,?,?)", (x[0], y[0], y[1]))


sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()