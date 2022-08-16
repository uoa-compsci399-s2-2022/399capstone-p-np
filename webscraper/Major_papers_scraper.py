
import urllib.request as urlrq
import certifi
import ssl
import numpy as np
from unicodedata import normalize
from bs4 import BeautifulSoup
import json

#This is required above normal website reading as the SSL certificate has a problem
#Downloads website as HTML and reads it with BeautifulSoup
def downloadinfo(url):
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
    courses = soup.find_all("div", class_="coursePaper section")
    for course in courses:
        code = course.find("div", class_="courseA").text.strip()
        title = course.find("div", class_="points").text.strip()
        descrition = course.find("p", class_="description").text.strip()

        #Uses a loop to find all the pre_reqs as their own list
        pre_reqs = [x.text.strip() for x in course.find_all("p", class_="prerequisite")]

        course_info.append([code, title,descrition,pre_reqs])

    return course_info
    

def scrape_subject_links(url):
    response = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    strhtm = soup.prettify()
    course_info = []
    courses = soup.find_all("div", class_="badge-text")
    for course in courses:
        major_name = url.split("/")[len(url.split("/"))-1]
        major_name = major_name[:-5]
        course_info.append([course.find("a").text.strip(), course.find("a")["href"], url, major_name])
    return course_info 

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
#Writes file to JSON object 
json_object = json.dumps(list_of_subjects, indent=4)
with open("all_courses.json", "w") as outfile:
    outfile.write(json_object)

#Writes the courses and information into a dictionary
total = 0
all_course_info = {}
for subject in list_of_subjects:
    papers = downloadinfo(subject[1]) 
    total += len(papers)
    if (papers != []):
        name = "{}:{}".format(subject[3],subject[0])
        all_course_info.update({name:papers})
    print("{} papers recorded, {} finished ".format(total, name))

#Saves all course information into a .JSON
json_object = json.dumps(all_course_info, indent=4)
with open("course_information.json", "w") as outfile:
    outfile.write(json_object)
