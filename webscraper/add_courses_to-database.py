import json
import sqlite3
  
# Opening JSON file
f = open('course_information.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)





database = r"C:\Users\windows\Documents\GitHub\399capstone-p-np\399courses.db"



sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""DELETE FROM course where 1= 1;""")

sqlite_insert_query = """INSERT INTO course
                      (subject, courseNumber, Bsc, Bsa, pointsValue, GPAreq, level, approvalNeeded, description) 
                       VALUES 
                      (?,?,?,?,?,?,?,?,?);"""

names = list(data.keys())
counter = 0
for name in names:
    for course in data[name]:
        courseID = course[0].split(" ")[0]
        courseNumber = course[0].split(" ")[1]
        coursePoints = float(course[1].split(" ")[0])
        courseDesc = course[2]

        data_tuple = (courseID,courseNumber,1,0,coursePoints,0,100,0,courseDesc)
        cursor.execute(sqlite_insert_query, data_tuple)
        
        print(courseID, courseNumber, " ", counter)
        counter += 2
sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()
