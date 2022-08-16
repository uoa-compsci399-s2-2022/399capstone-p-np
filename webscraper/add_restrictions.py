import json
import sqlite3
import re

f = open('all_courses.json')
data = json.load(f)
course_names = data[0]
courseID = data[1]

f = open('all_courses.json')
data = json.load(f)

for name in names:
    for course in data[name]:
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
                for x in clean_req.split(" ")[1:]:
                    print("hi")
                    if x not in course_names and x not in courseID and x not in ["and", "or"]:
                        break
                    else:
                        for restriction in clean_req.split(" ")[1:]:
                            if restriction in coursenames:
                                currentSubject = restriction
                            else:
                                currentID = restriction
                                restrictions.append((mainSubject, mainID, currentSubject, currentID))




