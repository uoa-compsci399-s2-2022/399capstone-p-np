from re import sub
import sqlite3
import os

class execute:
    def __init__(self):
        self.__sqliteConnection = sqlite3.connect("\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("library") + 1]) + "\\adapters\\399courses.db")
        self.__cursor = self.__sqliteConnection.cursor()

    def data_fetch(self):
        db_menu = self.__cursor.execute('select * from course').fetchall()
        return db_menu

    def list_all_majors(self):
        self.__cursor.execute("select * from majorRequirements")
        rows = self.__cursor.fetchall()
        return rows

    def delete_course(self, subject, courseNumber):
        self.__cursor.execute('delete from course where subject = ? and courseNumber = ?', (subject, courseNumber))
        self.__sqliteConnection.commit()

    def insert_paper_to_database(self, appendlist):
        self.__cursor.execute('insert into course values(?,?,?,?,?,?,?,?,?,?,?,?)', appendlist)
        self.__sqliteConnection.commit()

    def update_course(self, MajorType, pointsValue, GPAreq, level, approvalNeeded, description, problematicPreReqs, problematicRestrictions, problematicCoReqs, problematicOther, subject, courseNumber):
        sql_update_query = 'update course set MajorType=?, pointsValue=?, GPAreq=?, level=?, approvalNeeded=?, description=?, problematicPreReqs=?, problematicRestrictions=?, problematicCoReqs=?, problematicOther=? where subject=? and courseNumber=?'
        self.__cursor.execute(sql_update_query, (MajorType, pointsValue, GPAreq, level, approvalNeeded, description, problematicPreReqs, problematicRestrictions, problematicCoReqs, problematicOther, subject, courseNumber))
        self.__sqliteConnection.commit()

    def update_majorreq(self, majorName, totalPointsNeeded, pointsGenEd, year, honours, level, pointsAboveStage1, pointsAboveStage2, miscProblems, majorID):
        sql_update_query = 'update majorRequirements set majorName=?, totalPointsNeeded=?, pointsGenEd=?, year=?, honours=?, level=?, pointsAboveStage1=?, pointsAboveStage2=?, miscProblems=? where majorID=?'
        self.__cursor.execute(sql_update_query, (majorName, totalPointsNeeded, pointsGenEd, year, honours, level, pointsAboveStage1, pointsAboveStage2, miscProblems, majorID))
        self.__sqliteConnection.commit()
