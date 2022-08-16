import json
import sqlite3
import re
import traceback
import sys



print("hi")
# Opening JSON file
f = open('course_information.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

import os
database = os.path.abspath(os.getcwd())
print(database)


names = list(data.keys())

database = r"C:\Users\Zachary\Desktop\web\399courses.db"
database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\399courses.db"


sqliteConnection = sqlite3.connect(database)

cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""DELETE FROM course where 1= 1;""")

sqlite_insert_query = """INSERT INTO course
                      (subject, courseNumber, MajorType, pointsValue, GPAreq, level, approvalNeeded, description) 
                       VALUES 
                      (?,?,?,?,?,?,?,?);"""


coursenames = []
courseids = []
counter = 0
for name in names:
    for course in data[name]:
        #print(course)
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
        
        data_tuple = (courseID,courseNumber,name.split("_")[0],coursePoints,courseGPA,courseLevel,courseApproval,courseDesc)
        
        try:
            cursor.execute(sqlite_insert_query, data_tuple)
        except sqlite3.IntegrityError as er:
            print("Don't worry:", er.args[0], courseID,courseNumber)
            '''print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))'''
            #print(data_tuple)

        coursenames.append(courseID)
        courseids.append(courseNumber)
        #print(courseID, courseNumber," ", courseLevel , " ", courseGPA," ", counter)
        counter += 2
sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()


coursenames = list(set(coursenames))
courseids = list(set(courseids))

with open('course_name_and_IDs.json', 'w') as outfile:
    json.dump([coursenames,courseids], outfile)








