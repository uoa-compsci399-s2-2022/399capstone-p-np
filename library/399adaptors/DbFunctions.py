import os
import sqlite3
import time

class searchTool:
    def __init__(self):
        #sqliteConnection = sqlite3.connect(os.path.abspath(os.getcwd()) + "\\data\\399courses.db")
        database = r"C:\Users\Zachary\Documents\GitHub\399capstone-p-np\library\adapters\399adaptors\data\399courses.db"
        sqliteConnection = sqlite3.connect(database)
        self.__cursor = sqliteConnection.cursor()


    def return_all_courses(self):
        a = self.__cursor.execute("select * from course")
        course = a.fetchall()
        newlist = []
        for x in course:
            newlist.append((x[0],x[1]))
        return newlist

    def return_isolated_problems_with_course(self, course_subject, course_number):
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            new_str = ""
            for x in course[8:]:
                if x != None:
                    new_str = new_str + x
            return new_str
        else:
            return "does not exist"

    def return_course_description(self, course_subject, course_number):
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            return course[7]
        else:
            return "does not exist"

    def return_all_course_information(self, course_subject, course_number):
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            return course
        else:
            return "does not exist"

    def return_course_points(self, course_subject, course_number):
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            return course[3]
        else:
            return "does not exist"

    def problems_with_course(self, courseName, courseNumber, timetable):
        #the timetable is given as a list of all subjects done in (y1S1, y1S2, y2s1, y2s2)
        timetable = []
        done_courses = []
        doing = []
        for sem in timetable:
            if (courseName, courseNumber) not in sem:
                for course in sem:
                    timetable.append(course)
            else:
                doing = sem
                exit

        problems_with_course = {}

        a = self.__cursor.execute("select * from preReq where preReqSubject = ? and preReqNumber = ?", (courseName, courseNumber))
        problems_with_course.update({"prereqs" : [(x[2],x[3]) for x in a.fetchall() if (x[2],x[3]) not in done_courses]})

        a = self.__cursor.execute("select * from restriction where restrictionSubject = ? and restrictionNumber = ?", (courseName, courseNumber))
        problems_with_course.update({"restrictions" : [(x[2],x[3]) for x in a.fetchall() if (x[2],x[3]) in done_courses or (x[2],x[3]) in doing]})

        a = self.__cursor.execute("select * from corequisite where corequisiteSubject = ? and corequisiteNumber = ?", (courseName, courseNumber))
        problems_with_course.update({"corequisite" : [(x[2],x[3]) for x in a.fetchall() if (x[2],x[3]) not in doing]})

        problems_with_course.update({"other_problems": self.return_isolated_problems_with_course(courseName, courseNumber)})

        print(problems_with_course)
        return (problems_with_course)
    
    def worst_problems_with_course(self, courseName, courseNumber, timetable):
        done_courses = []
        doing = []
        for semester in timetable:
            
            if (courseName, courseNumber) not in semester:
                for course in semester:
                    done_courses.append(course)
            else:
                for course in semester:
                    
                    doing.append(course)

        a = self.__cursor.execute("select * from preReq where subject = ? and courseNumber = ?", (courseName, courseNumber))
        res = [(x[0],str(x[1])) for x in a.fetchall()]
        for pre in res:
            if pre not in done_courses:
                return "You need to take: " + pre[0] + " " + pre[1]
        
        a = self.__cursor.execute("select * from restriction where restrictionSubject = ? and restrictionNumber = ?", (courseName, courseNumber))
        res = [(x[0],str(x[1])) for x in a.fetchall()]
        for pre in res:
            if  pre in doing or pre in done_courses:
                return "You cannot take: " + pre[0] + " " + pre[1]

        a = self.__cursor.execute("select * from corequisite where subject = ? and courseNumber = ?;", (courseName, courseNumber))
        res = [(x[0],str(x[1])) for x in a.fetchall()]
        for pre in res:
            if pre not in doing:
                return "You need to take: " + pre[0] + " " + pre[1]
        return ""

    def problems_with_timetable(self, timetable):
        new_timetable = []
        probs = []
        for sem in timetable:
            new_timetable.append(sem)
            probs.append([[course[0]+ " " + course[1], self.worst_problems_with_course(course[0],course[1], new_timetable),self.return_isolated_problems_with_course( course[0],  course[1]) ] for course in sem])
        return probs

    def will_graduate(self, timetable):
        probs = self.problems_with_timetable(timetable)
        for x in probs:
            if x[1] != "":
                return False
        return True
    


a = searchTool()
tim = [[("COMPSCI", "101"),("COMPSCI", "120"),("COMPSCI", "130"),("PHYSICS", "140")],[("COMPSCI", "215"),("COMPSCI", "220"),("COMPSCI", "230"),("PHYSICS", "240")],[("COMPSCI", "313")]]
print(a.worst_problems_with_course("INFOGOV", "706",[[("INFOGOV", "706")]] ))

#z = a.problems_with_timetable([[("COMPSCI", "101"),("COMPSCI", "120"),("COMPSCI", "130"),("PHYSICS", "140")],[("COMPSCI", "215"),("COMPSCI", "220"),("COMPSCI", "230"),("PHYSICS", "240")],[("COMPSCI", "313")]])
#for x in z:
#    for y in x:
#        print (y)