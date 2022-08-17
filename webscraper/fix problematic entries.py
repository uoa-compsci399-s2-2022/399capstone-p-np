import json
import sqlite3
import re


#use OS to change path dynamically
database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\399courses.db"


#Connects to database file
sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")


#The SQL query, the ?s are the data
sqlite_insert_query = """INSERT INTO restriction
                      (restrictionSubject, restrictionNumber, subject, courseNumber) 
                       VALUES 
                      (?,?,?,?);"""

#List of tuples for insertion
final_list_of_rest = [("this", "is", "a", "test")]

#calls the SQL command here. If key duplication error then its fine. Anything else is an issue
for x in final_list_of_rest:
    try:
        cursor.execute(sqlite_insert_query, x)
    except sqlite3.IntegrityError as er:
        print("Don't worry:", er.args[0], x)

#Commits and saves.
sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()



""" 
If you aren't sure how to process the problematicRestriction, you can just leave it there. 
I think there are some leading spaces on some of them
You can trust the course_name_and_IDs.JSON file to exist and be up to date. 
If they have a restriction of a course that doesn't exist you can ignore it. (Or add it to a seperate table in the database for admins to review)

f = open('course_name_and_IDs.json')
data = json.load(f)
course_names = data[0]
courseID = data[1]

To read the data probably use something like this https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

There will also be problematic pre-reqs, co-reqs and approval needed.
"""