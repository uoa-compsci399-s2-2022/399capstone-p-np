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
    

requriment_pointers = [
    ["Restriction:","restrictionSubject", "restrictionNumber", "problematicRestrictions","restriction"],
    ["Prerequisite:","preReqSubject", "preReqNumber", "problematicPreReqs","preReq"],
    ["Corequisite:","corequisiteSubject", "corequisite", "problematicCoReqs","corequisite"]
]
for requriment_pointer in requriment_pointers:
    final_list_of_rest = []   
    problematics = []    
    for course in all_courses_list:
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
                            final_list_of_rest.append((requriment_pointer[4],requriment_pointer[1],requriment_pointer[2],main_subj.split(" ")[0], main_subj.split(" ")[1], rest_subj, x))



    database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\399courses.db"


    sqliteConnection = sqlite3.connect(database)

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_append_query = """UPDATE course
    set ? = ?
    where courseNumber = ? and lower(subject) = lower(?);"""
    for x in problematics:
        tupER = ((requriment_pointer[3], x[1], x[0].split(" ")[1], x[0].split(" ")[0]))
        tupER = ((requriment_pointer[3], "test", x[0].split(" ")[1], x[0].split(" ")[0]))
        print(tupER)
        cursor.execute(sqlite_append_query, tupER)

    sqliteConnection.commit()
    sqlite_insert_query = """INSERT INTO ?
                        (?, ?, subject, courseNumber) 
                        VALUES 
                        (?,?,?,?);"""

    for x in final_list_of_rest:
        try:
            cursor.execute(sqlite_insert_query, x)
        except sqlite3.IntegrityError as er:
            print("Don't worry:", er.args[0], x)
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

        




