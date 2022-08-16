import json
import sqlite3
import re

f = open('course_name_and_IDs.json')
data = json.load(f)
course_names = data[0]
courseID = data[1]
f = open('course_information.json')
course_information = json.load(f)

names = list(course_information.keys())

all_courses_list = []
for name in names:
    for x in course_information[name]:
        all_courses_list.append(x)
        
for course in all_courses_list:
    for req in course[3]:
        if req.split(" ")[0] == "Restriction:":
            restrictions = []
            clean_req =  " ".join(req.split(" ")[1:])
            clean_req=re.sub(",","",clean_req)
            mainSubject = course[0]
            mainID = course[1]
            currentSubject = "This is Problematic"
            currentID = "this is also problematic"
            word_num = 0
            
            while word_num < len(clean_req.split(" ")[1:]):
                
                x =clean_req.split(" ")[1:][word_num]
                if x not in course_names and x not in courseID:
                    print(x)
                    word_num = 10000000000000
                else:
                    for restriction in clean_req.split(" ")[1:]:
                        if restriction in course_names:
                            currentSubject = restriction
                        else:
                            currentID = restriction
                            restrictions.append((mainSubject, mainID, currentSubject, currentID))
                word_num += 1




