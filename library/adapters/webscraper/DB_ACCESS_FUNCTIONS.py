from re import sub
import sqlite3
import os

class execute:
    def __init__(self):
        self.__sqliteConnection = sqlite3.connect("\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("399capstone-p-np") + 1]) + "\\library\\adapters\\399courses.db")
        self.__cursor = self.__sqliteConnection.cursor()

    def list_all_majors(self):
        self.__cursor.execute("SELECT majorID from majorRequirements")
        rows = self.__cursor.fetchall()
        return rows

    def delete_course(self, subject, courseNumber):
        sqlite_del = """DELETE FROM course where subject = ? and courseNumber = ?"""
        self.__cursor.execute(sqlite_del, (subject, courseNumber))
        self.__sqliteConnection.commit()

    def insert_paper_to_database(self, subject, courseNumber, MajorType, pointsValue, GPAreq, level, approvalNeeded, description):
        
        sqlite_insert_query = """INSERT INTO course
                            (subject, courseNumber, MajorType, pointsValue, GPAreq, level, approvalNeeded, description) 
                            VALUES 
                            (?,?,?,?,?,?,?,?);"""
        self.__cursor.execute(sqlite_insert_query, (subject, courseNumber, MajorType, pointsValue, GPAreq, level, approvalNeeded, description))
        self.__sqliteConnection.commit()



#cursor.close()