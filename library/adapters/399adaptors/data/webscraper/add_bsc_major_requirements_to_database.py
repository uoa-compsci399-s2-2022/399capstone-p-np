import json
import sqlite3
import re

f = open('major_reqs.json')
major_reqs = json.load(f)



database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\library\adapters\399adaptors\data\399courses.db"


sqliteConnection = sqlite3.connect(database)

cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

major_reqs = open('major_reqs.json')
major_information = json.load(major_reqs)

query = """INSERT INTO majorRequirements(majorName, totalPointsNeeded, pointsGenEd, year, honours, level) VALUES(?, ?, ?, ?, ?, ?)"""
for major in major_information:
    total = 0
    for groups in major[1:]:
        for group in groups:
            if len(group[0]) == 1:
                total += int(group[0][0])

    if "before-2019" in major[0][0][2]:
        year = 2018
    else:
        year = 2020
    
    if "hon" in major[0][0][2]:
        honours = 1
    else:
        honours = 0
 

    cursor.execute(query, (major[0][0][0], total, 30, year, honours, major[0][0][1]))
    sqliteConnection.commit()

cursor.close()
print("successful")
