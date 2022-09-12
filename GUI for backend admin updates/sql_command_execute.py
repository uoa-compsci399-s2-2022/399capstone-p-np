import sqlite3

class execute:
    def __init__(self):
        database = "399courses.db"
        self.__sqliteConnection = sqlite3.connect(database)
        self.__cursor = self.__sqliteConnection.cursor()

    def data_fetch(self):
        db_menu = self.__cursor.execute('select * from course').fetchall()
        return db_menu

    def list_all_majors(self):
        self.__cursor.execute("select majorID from majorRequirements")
        rows = self.__cursor.fetchall()
        return rows

    def delete_course(self, subject, courseNumber):
        self.__cursor.execute('delete from course where subject = ? and courseNumber = ?', (subject, courseNumber))
        self.__sqliteConnection.commit()

    def insert_paper_to_database(self, appendlist):
        self.__cursor.execute('insert into course values(?,?,?,?,?,?,?,?,?,?,?,?)', appendlist)
        self.__sqliteConnection.commit()
