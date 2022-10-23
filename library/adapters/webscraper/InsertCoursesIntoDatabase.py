import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
import sqlite3
import traceback
import sys
import os

print("Inserting all courses and requirements into the database.")

#Initalizing connection to the database
database = os.path.abspath(os.getcwd())
database = "\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("399capstone-p-np") + 1]) + "\\library\\adapters\\399courses.db"
sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")


print("Deleting old data from database") #Deleting old data from database
cursor.execute("""DELETE FROM course where 1= 1;""")
cursor.execute("""delete from restriction where 1 = 1""")
cursor.execute("""delete from preReq where 1 = 1""")
cursor.execute("""delete from corequisite where 1 = 1""")
cursor.execute("""UPDATE course set problematicPreReqs = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicRestrictions = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicCoReqs = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicOther = NULL where 1=1;""")


#This function takes a list of courses in the calendar and writes all information into a list
def downloadinfo(url):
    #Tries to create connectio to HTML
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
    
    #Reads HTML and parses with beautifulsoup
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
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
    
#This function takes as input a faculty and then returns all URLs to lists of courses within said faculty
def scrape_subject_links(url):
    response = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    course_info = []
    courses = soup.find_all("div", class_="badge-text")
    for course in courses:
        major_name = url.split("/")[len(url.split("/"))-1]
        major_name = major_name[:-5]
        course_info.append([course.find("a").text.strip(), course.find("a")["href"], url, major_name])

    return course_info 

#Adds all URLs to all subjects the university offers
list_of_subjects = []
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-medical-and-health-sciences.html")
list_of_subjects =  scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-arts.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-science.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-business-and-economics.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-creative-arts-and-industries.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-education-and-social-work.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-engineering.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-law.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/faculty-of-medical-and-health-sciences.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/general-education.html")
list_of_subjects += scrape_subject_links("https://www.calendar.auckland.ac.nz/en/courses/the-university-of-auckland.html")

sqlite_insert_query = """INSERT INTO course
                      (subject, courseNumber, MajorType, pointsValue, GPAreq, level, approvalNeeded, description) 
                       VALUES 
                      (?,?,?,?,?,?,?,?);"""

course_names = []
course_ids = []

#Parses course info into a list of different requirment types
def deal_with_req(course):
    courseID = course[0].split(" ")[0]
    courseNumber = course[0].split(" ")[1]
    requirements = course[3]
    reqirment_data = [courseID,courseNumber,"","","",""]
    for req in requirements:
        if req.split(" ")[0] == "Restriction:":
            reqirment_data[2] = req.replace(",","")
        if req.split(" ")[0] == "Prerequisite:":
            reqirment_data[3] = req.replace(",","")
        if req.split(" ")[0] == "Corequisite:":
            reqirment_data[4] = req.replace(",","")
        else:
            reqirment_data[5] = req
    return reqirment_data

#Gets the course data cleans it and adds it to the database.
paper_number = 0
requirement_data = []
for subject in list_of_subjects:
    #Downloads all information from a subject and returns it as a matrix, is not cleaned
    papers = downloadinfo(subject[1]) 
    for course in papers:
        paper_number += 1

        #seperates the requriements
        requirement_data.append(deal_with_req(course))

        #seperates out the coursename and ID
        courseID = course[0].split(" ")[0]
        courseNumber = course[0].split(" ")[1]

        #adds the coursenames and ids to a final list for future reference
        course_names.append(courseID)
        course_ids.append(courseNumber)
        
        #Finds out the course level
        if sum(c.isdigit() for c in courseNumber) >=3 and courseNumber[0] in "0123456789":
            courseLevel = int(courseNumber[0] + "00")
        else:
            courseLevel = 0

        #Tries to scrape the course GPA if possible
        courseGPA = 0
        for x in course[3]:
            if "gpa" in x.lower():
                try:
                    words = x.lower().split(" ")
                    z = 0
                    for h in words:
                        if h == "gpa":
                            location = z
                        z += 1
                    courseGPA = float(words[location + 2])
                except:
                    courseGPA = 0
        if courseGPA > 9 or courseGPA < 0:
            courseGPA = 0

        #Gets course points and description
        coursePoints = float(course[1].split(" ")[0])
        courseDesc = course[2]
        
        #Tries to insert course and all data into database
        data_tuple = (courseID,courseNumber,subject[3].split("_")[0],coursePoints,courseGPA,courseLevel,"",courseDesc)
        try:
            cursor.execute(sqlite_insert_query, data_tuple)
            print("{:13} inserted from {:39} {:.2%} finished".format(courseID+courseNumber,  subject[-1],(paper_number/7000)))
        except sqlite3.IntegrityError as er:
            print("Don't worry:", er.args[0], courseID,courseNumber)

#Defines SQL queries to append restrictions
Restriction =  """UPDATE course set problematicRestrictions = ? where courseNumber = ? and lower(subject) = lower(?);"""
Prerequisite = """UPDATE course set problematicPreReqs      = ? where courseNumber = ? and lower(subject) = lower(?);"""
Corequisite =  """UPDATE course set problematicCoReqs       = ? where courseNumber = ? and lower(subject) = lower(?);"""
other =        """UPDATE course set problematicOther        = ? where courseNumber = ? and lower(subject) = lower(?);"""

RestrictionIns =  """INSERT INTO "restriction"   (restrictionSubject, restrictionNumber, subject, courseNumber) VALUES (?,?,?,?);"""
PrerequisiteIns = """INSERT INTO "preReq"        (preReqSubject, preReqNumber, subject, courseNumber) VALUES (?,?,?,?);"""
CorequisiteIns =  """INSERT INTO "corequisite"   (corequisiteSubject, corequisiteNumber, subject, courseNumber) VALUES (?,?,?,?);"""

requriment_pointers = [
    [RestrictionIns, Restriction, 2],
    [PrerequisiteIns, Prerequisite, 3],
    [CorequisiteIns, Corequisite, 4]
]

#Takes a sentence of restrictions and splits it into a list of restrictionNames+Ids
def normalize(sentence):
    new = []
    current_id = ""
    current_subject = ""
    for x in sentence.split(" "):
        if x in course_names:
            current_id = ""
            current_subject = x
        if x in course_ids:
            current_id = x
        if current_id != "" and current_subject != "":
            new.append((current_subject,current_id))
    return new

#This part is dealing with the requirements for each course. 
for type in requriment_pointers:
    for course in requirement_data:
        for x in [z for z in course[type[2]].split(" ") if z != ""]:
            #This checks that there is not english words I cannot understand. It will overwrite (ISSUE) the old data and put the new data in the correct positoin in majorrequirements
            if x not in ["Restriction:","Corequisite:", "Prerequisite:"] + course_ids + course_names:
                print(course[type[2]],course[0],course[1])
                cursor.execute(type[1], (course[type[2]],course[1],course[0]))
                break

        #This is a for else loop. If there is only words we do understand then it can add data to the prereq, coreq and restriction table
        else:
            for inner_reqs in normalize(course[type[2]]):
                try:
                    #Normalizes the data into the right format and tries to insert it. 
                    cursor.execute(type[0],(inner_reqs[0],inner_reqs[1],course[0],course[1]))
                except sqlite3.IntegrityError as er:
                    #Error messages if something went wront. Usually this is the unique constraint
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    print('SQLite traceback: ')
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    print(traceback.format_exception(exc_type, exc_value, exc_tb))

#Adds miscilanious restrictions to problematicOther in MajorRequirements
for course in requirement_data:
    cursor.execute(other,(course[5],course[1],course[0]))
    
#commits and saves changes to DB
sqliteConnection.commit()
print("Records inserted successfully into 399courses.db")
cursor.close()