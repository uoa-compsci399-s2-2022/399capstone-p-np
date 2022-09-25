import json
import sqlite3
import re

f = open('major_reqs.json')
major_reqs = json.load(f)



database = r"C:\Users\windows\Documents\GitHub\399capstone-p-np\library\399adaptors\399courses.db"


sqliteConnection = sqlite3.connect(database)

cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

cursor.execute("""DELETE FROM "majorRequirements" """)
cursor.execute("""DELETE FROM "group" """)
cursor.execute("""DELETE FROM "majorGroupLink" """)
cursor.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='majorRequirements' """)
cursor.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='group' """)

major_reqs = open('major_reqs.json')
major_information = json.load(major_reqs)

query = """INSERT INTO majorRequirements(majorName, totalPointsNeeded, pointsGenEd, year, honours, level) VALUES(?, ?, ?, ?, ?, ?)"""
for major in major_information:
    total = 0
    for groups in major[1:]:
        for group in groups:
            if len(group[0]) == 1:
                total += int(group[0][0])

    if "from-2019" in major[0][0][2]:
        year = 2020
    else:
        year = 2018
    
    if "hon" in major[0][0][2]:
        honours = 1
    else:
        honours = 0
 

    cursor.execute(query, (major[0][0][0], total, 30, year, honours, major[0][0][1]))
    sqliteConnection.commit()



for major in major_information:
    if "from-2019" in major[0][0][2]:
        year = 2020
    else:
        year = 2018
    if "hon" in major[0][0][2]:
        honours = 1
    else:
        honours = 0
    cursor.execute("""SELECT majorID FROM majorRequirements WHERE majorName = ? AND  honours = ? AND year = ?""", (major[0][0][0], honours, year))
    majorID = cursor.fetchall()[0]
    print(majorID)
    groupID = 0
    for groups in major[1:]:
        for group in groups:
            groupID += 1
            if len(group[0]) == 1:
                cursor.execute("""INSERT INTO majorGroupLink("majorID", "groupID", pointsRequired) VALUES(?, ?, ?)""", (majorID[0], groupID, group[0][0]))
                for course in group[1:]:
                    cursor.execute("""INSERT INTO "group"(groupID, majorID, courseNumber, subject) VALUES(?, ?, ?, ?)""", (groupID, majorID[0], course[1], course[0]))
            else:
                cursor.execute("""INSERT INTO majorGroupLink("majorID", "groupID", pointsRequired) VALUES(?, ?, ?)""", (majorID[0], groupID, "ERROR SCRAPING DATA"))
            sqliteConnection.commit()

cursor.close()
print("successful")
