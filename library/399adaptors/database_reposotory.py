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
sqlite_insert_query = """select pointsrequired majorname from majors;"""


#calls the SQL command here. If key duplication error then its fine. Anything else is an issue

c = cursor.execute(sqlite_insert_query)


rows = result.fetchall();

#Commits and saves.
sqliteConnection.commit()
print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()



#list of all possible courses that exit
#a function of all courses they need to take to graduate required courses,(group courses, points))
#given name of courses they are taking and what time, return same matrix with null, or error message
#given list of courses if they will graduate
#Return all courses that can be taken at that time
#return a list of courses they can take given what they are doing
#Returns unclassified errors with a specific course
#given a course return course description
#given a coure return all course information
