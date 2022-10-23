import GenerateDatabaseTables
import InsertCoursesIntoDatabase
import InsertGenEdsToDatabase
import ScrapeMajorRequirementsJSON
import AddMajorRequirementsToDatabase

import sqlite3
import os


database = "\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("library") + 1]) + "\\adapters\\399courses.db"
sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()

#THIS ASSUMES EVERYTHING IS A SCIENCE MAJOR
cursor.execute("""  DELETE FROM scheduleMajorLink
WHERE 1==1; """)

cursor.execute("""  DELETE FROM preReqGroup
WHERE 1==1; """)

cursor.execute("""insert into scheduleMajorLink (scheduleID, majorID)
select scheduleID, majorRequirements.majorID from  schedule 
inner join majorRequirements 
on scheduleID == "Open Schedule"
or scheduleID == "Engineering, Medical and Health Sciences, Science (EMHSS) Schedule";""")


cursor.execute("""insert into "group"(groupID, majorID, subject, courseNumber)
Values (13, 10, "COMPSCI", "399");""") 

try:
    cursor.execute("""insert into "majorGroupLink"(groupID, majorID, pointsRequired)
    Values (13, 10, 15);""") 
except:
    pass

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "105", "COMPSCI", "210", "1",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "107", "COMPSCI", "210", "1",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "210", "1",15); """) 


cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "105", "COMPSCI", "215", "2",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "107", "COMPSCI", "215", "2",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "215", "2",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "105", "COMPSCI", "220", "3",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "107", "COMPSCI", "220", "3",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "220", "3",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "120", "COMPSCI", "220", "4",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS ", "120", "COMPSCI", "220", "4",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "105", "COMPSCI", "230", "5",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "107", "COMPSCI", "230", "5",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "230", "5",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "105", "COMPSCI", "235", "6",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "107", "COMPSCI", "235", "6",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "235", "6",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "110", "COMPSCI", "289", "7",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "120", "COMPSCI", "289", "8",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "130", "COMPSCI", "289", "8",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "225", "COMPSCI", "320", "9",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "254", "COMPSCI", "320", "9",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "230", "COMPSCI", "345", "10",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("SOFTENG", "206", "COMPSCI", "345", "10",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points") 
values("COMPSCI", "220", "COMPSCI", "350", "11",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("PHIL", "222", "COMPSCI", "350", "11",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "225", "COMPSCI", "350", "12",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "254", "COMPSCI", "350", "12",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points") 
values("COMPSCI", "225", "COMPSCI", "351", "13",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "254", "COMPSCI", "351", "13",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("DATASCI", "100", "COMPSCI", "361", "14",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("STATS", "101", "COMPSCI", "361", "14",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("STATS", "108", "COMPSCI", "361", "14",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "225", "COMPSCI", "361", "15",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "254", "COMPSCI", "361", "15",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "255", "COMPSCI", "361", "15",15); """) 

cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("MATHS", "254", "COMPSCI", "367", "16",15); """) 
cursor.execute("""INSERT into preReqGroup("preReqSubject", "preReqNumber", "subject" , "courseNumber","groupID", "points")
values("COMPSCI", "225", "COMPSCI", "367", "16",15); """) 

cursor.execute("""UPDATE majorRequirements
SET totalPointsNeeded = 360
WHERE
      "level" = "undergraduate" """) 


sqliteConnection.commit()
cursor.close()

