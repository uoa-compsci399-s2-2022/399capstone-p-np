import json
import sqlite3
import re
import os

database = "\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("399capstone-p-np") + 1]) + "\\library\\adapters\\399courses.db"

if os.path.exists(database):
  os.remove(database)
  print("Deleted old SQLite Database file")

print("Creating new database file")
sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()

print("Creating tables")
cursor.execute("""
CREATE TABLE "corequisite" (
    "corequisiteSubject"    char NOT NULL,
    "corequisiteNumber"    int NOT NULL,
    "subject"    char NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    PRIMARY KEY("subject","courseNumber","corequisiteSubject","corequisiteNumber"),
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber"),
    FOREIGN KEY("corequisiteSubject","corequisiteNumber") REFERENCES "course"("subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "course" (
    "subject"    CHAR NOT NULL,
    "courseNumber"    char NOT NULL,
    "MajorType"    char,
    "pointsValue"    REAL,
    "GPAreq"    ,
    "level"    int,
    "approvalNeeded"    char,
    "description"    TEXT, problematicPreReqs TEXT, problematicRestrictions TEXT, problematicCoReqs TEXT, problematicOther text,
    PRIMARY KEY("subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "courseInstance" (
    "subject"    char NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    "courseYear"    INTEGER NOT NULL,
    "courseSemester"    INTEGER NOT NULL,
    "courseLecturer"    char,
    "courseCoordinator"    char,
    "courseTutors"    char,
    PRIMARY KEY("courseYear","courseSemester","subject","courseNumber"),
    FOREIGN KEY("courseNumber","subject") REFERENCES "course"("courseNumber","subject")
);""")

cursor.execute("""
CREATE TABLE "coursePreReqGroup" (
    "subject"    CHAR NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    "groupID"    char NOT NULL,
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber"),
    FOREIGN KEY("groupID") REFERENCES "majorGroupLink",
    PRIMARY KEY("groupID","subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "courseScheduleLink" (
    "scheduleID"    CHAR NOT NULL,
    "subject"    char NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    PRIMARY KEY("scheduleID","subject","courseNumber"),
    FOREIGN KEY("scheduleID") REFERENCES "schedule"("scheduleID"),
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "group" (
    "groupID"    INTEGER NOT NULL,
    "majorID"    INTEGER NOT NULL,
    "courseNumber"    CHAR,
    "subject"    CHAR,
    "reqID"    INTEGER,
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber"),
    PRIMARY KEY("reqID" AUTOINCREMENT)
);""")

cursor.execute("""
CREATE TABLE "majorGroupLink" (
    "majorID"    INTEGER NOT NULL,
    "groupID"    INTEGER NOT NULL,
    "pointsRequired"    TEXT,
    PRIMARY KEY("majorID","groupID")
)""")

cursor.execute("""
CREATE TABLE "majorRequirements" (
	"majorID"	INTEGER UNIQUE,
	"majorName"	TEXT NOT NULL,
	"totalPointsNeeded"	CHAR,
	"pointsGenEd"	REAL NOT NULL,
	"year"	INTEGER NOT NULL,
	"honours"	INTEGER NOT NULL,
	"level"	TEXT,
	"pointsAboveStage1"	INTEGER,
	"pointsAboveStage2"	INTEGER,
	PRIMARY KEY("majorID" AUTOINCREMENT)
);""")

cursor.execute("""
CREATE TABLE "neededCourses" (
    "majorID"    CHAR NOT NULL,
    "subject"    char NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    FOREIGN KEY("majorID") REFERENCES "majorRequirements",
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber"),
    PRIMARY KEY("majorID","subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "preReq" (
    "preReqSubject"    CHAR NOT NULL,
    "preReqNumber"    CHAR NOT NULL,
    "subject"    CHAR NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    PRIMARY KEY("subject","courseNumber","subject","courseNumber"),
    FOREIGN KEY("preReqSubject","preReqNumber") REFERENCES "course"("subject","courseNumber"),
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE "restriction" (
    "restrictionSubject"    char NOT NULL,
    "restrictionNumber"    int NOT NULL,
    "subject"    char NOT NULL,
    "courseNumber"    CHAR NOT NULL,
    PRIMARY KEY("subject","courseNumber","restrictionSubject","restrictionNumber"),
    FOREIGN KEY("subject","courseNumber") REFERENCES "course"("subject","courseNumber"),
    FOREIGN KEY("restrictionSubject","restrictionNumber") REFERENCES "course"("subject","courseNumber")
);""")

cursor.execute("""
CREATE TABLE schedule
( scheduleID CHAR not NULL,
  scheduleName char,
  scheduleDesc char,
  PRIMARY key (scheduleID)
 
  );""")


cursor.execute("""
CREATE TABLE scheduleMajorLink
( scheduleID CHAR not NULL,
  majorID int,
  PRIMARY key (scheduleID, majorID),
  FOREIGN KEY("majorID") REFERENCES "majorRequirements"("majorID"),
  FOREIGN KEY("scheduleID") REFERENCES "courseScheduleLink"("scheduleID")
  );""")

print("created new tables")
sqliteConnection.commit()

cursor.close()
print("successful")
