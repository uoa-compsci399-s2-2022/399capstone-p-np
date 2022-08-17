import json
import sqlite3
import re
import time

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

database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\399courses.db"


sqliteConnection = sqlite3.connect(database)

cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""delete from restriction where 1 = 1""")
cursor.execute("""delete from preReq where 1 = 1""")
cursor.execute("""delete from corequisite where 1 = 1""")
cursor.execute("""UPDATE course set problematicPreReqs = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicRestrictions = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicCoReqs = NULL where 1=1;""")
cursor.execute("""UPDATE course set problematicOther = NULL where 1=1;""")
    
Restriction = """UPDATE course set problematicRestrictions = ? where courseNumber = ? and lower(subject) = lower(?);"""
Prerequisite = """UPDATE course set problematicPreReqs = ? where courseNumber = ? and lower(subject) = lower(?);"""
Corequisite = """UPDATE course set problematicCoReqs = ? where courseNumber = ? and lower(subject) = lower(?);"""

RestrictionIns =  """INSERT INTO "restriction"   (restrictionSubject, restrictionNumber, subject, courseNumber) VALUES (?,?,?,?);"""
PrerequisiteIns = """INSERT INTO "preReq" (preReqSubject, preReqNumber, subject, courseNumber) VALUES (?,?,?,?);"""
CorequisiteIns =  """INSERT INTO "corequisite"   (corequisiteSubject, corequisiteNumber, subject, courseNumber) VALUES (?,?,?,?);"""

requriment_pointers = [
    ["Restriction:","restrictionSubject", "restrictionNumber", Restriction,"restriction",RestrictionIns],
    ["Prerequisite:","preReqSubject", "preReqNumber", Prerequisite,"preReq",PrerequisiteIns],
    ["Corequisite:","corequisiteSubject", "corequisite", Corequisite,"corequisite",CorequisiteIns]
]
for requriment_pointer in requriment_pointers:
    final_list_of_rest = []   
    problematics = []    
    for course in all_courses_list:
        other_problems = ""
        for req in course[3]:
            if req.split(" ")[0] == requriment_pointer[0]:
                restrictions = []
                clean_req =  " ".join(req.split(" ")[1:])
                clean_req=re.sub(",","",clean_req)
                clean_req=clean_req.replace(".","")
                
                mainSubject = course[0]
                mainID = course[1]
                currentSubject = "P"
                currentID = "P"
                word_num = 0

                toadd = []
                temp_add = ''
                
                while word_num < len(clean_req.split(" ")[1:]):
                    temp_add = clean_req.split(" ")
                    x =clean_req.split(" ")[word_num]
                    if x not in course_names and x not in courseID:
                        problematics.append([course[0], clean_req])
                        word_num = 10000000000000
                        temp_add = ''
                    word_num += 1

                main_subj = course[0]
                main_id = course[1]

                if temp_add != '':
                    rest_subj = "bad"
                    rest_id = "bad"
                    for x in temp_add:
                        if x in course_names:
                            rest_subj = x
                        if x in courseID:
                            rest_id = x
                            final_list_of_rest.append((main_subj.split(" ")[0], main_subj.split(" ")[1], rest_subj, x))

            if req.split(" ")[0] not in ["Restriction:","Prerequisite:","Corequisite:"] :
                course_subject = course[0].split(" ")[0]
                course_number = course[0].split(" ")[1]
                query = """UPDATE course set problematicOther = ? where courseNumber = ? and lower(subject) = lower(?);"""
                other_problems = other_problems + req
                cursor.execute(query, (other_problems, course_number,course_subject))
                sqliteConnection.commit()


    

    

    sqlite_append_query = requriment_pointer[3]
    for x in problematics:
        tupER = ((x[1], x[0].split(" ")[1], x[0].split(" ")[0]))
        cursor.execute(sqlite_append_query, tupER)

    sqliteConnection.commit()
    sqlite_insert_query = requriment_pointer[5]
    print(sqlite_insert_query)

    for x in final_list_of_rest:
        try:
            cursor.execute(sqlite_insert_query, x)
        except:
            print("FAIL", x)
            pass

sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()

        




