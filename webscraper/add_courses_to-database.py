import json
import sqlite3
  
# Opening JSON file
f = open('course_information.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)



names = list(data.keys())

database = r"C:\Users\windows\Documents\GitHub\399capstone-p-np\399courses.db"



sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""DELETE FROM course where 1= 1;""")

sqlite_insert_query = """INSERT INTO course
                      (subject, courseNumber, Bsc, Bsa, pointsValue, GPAreq, level, approvalNeeded, description) 
                       VALUES 
                      (?,?,?,?,?,?,?,?,?);"""

coursenames = []
courseids = []
counter = 0
for name in names:
    for course in data[name]:
        courseID = course[0].split(" ")[0]
        courseNumber = course[0].split(" ")[1]
        if sum(c.isdigit() for c in courseNumber) >=3 and courseNumber[0] in "0123456789":
            courseLevel = int(courseNumber[0] + "00")
        else:
            courseLevel = 0

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

        courseApproval = ""
        for x in course[3]:
            if "approval" in x.lower():
                courseApproval = courseApproval + x[len("Prerequisite: "):]
                
                
        coursePoints = float(course[1].split(" ")[0])
        courseDesc = course[2]
        
        data_tuple = (courseID,courseNumber,1,0,coursePoints,courseGPA,courseLevel,courseApproval,courseDesc)
        cursor.execute(sqlite_insert_query, data_tuple)

        coursenames.append(courseID)
        courseids.append(courseNumber)
        #print(courseID, courseNumber," ", courseLevel , " ", courseGPA," ", counter)
        counter += 2
sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()


coursenames = list(set(coursenames))
courseids = list(set(courseids))








import re



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
                        
                for x in clean_req.split(" ")[1:]:
                    if x not in coursenames and x not in courseids and x not in ["and", "or"]:
                        break
                        #print(clean_req)
                    else:
                        
                        for restriction in clean_req.split(" ")[1:]:
                            if restriction in coursenames:
                                currentSubject = restriction
                            else:
                                currentID = restriction
                                
                                restrictions.append((mainSubject, mainID, currentSubject, currentID))
                                print((mainSubject, mainID, currentSubject, currentID))
                            
                #print(clean_req)





