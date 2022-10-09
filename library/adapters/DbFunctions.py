import os
import sqlite3
import time

class searchTool:
    def __init__(self):
        #sqliteConnection = sqlite3.connect(r"library\adapters\399courses.db")
        sqliteConnection = sqlite3.connect("\\".join(os.getcwd().split("\\")[:os.getcwd().split("\\").index("399capstone-p-np") + 1]) + "\\library\\adapters\\399courses.db")

        self.__cursor = sqliteConnection.cursor()


    def return_misc_problems_with_degree(self,major_type, year = "2020",honours = 0):
        
        a = self.__cursor.execute(
            """select miscProblems from majorRequirements where 
        majorRequirements.majorName = ? AND
        majorRequirements.year = ? AND
        majorRequirements.honours = ?;""",(major_type, year,honours))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 0:
            return []
        else:
            return [x[0] for x in list_of_courses]
    


    def return_all_courses(self):
        a = self.__cursor.execute("select * from 'course'")
        course = a.fetchall()
        newlist = []
        for x in course:
            newlist.append((x[0],x[1]))
        return newlist

    def return_isolated_problems_with_course(self, course_subject, course_number):
        #This function returns problems with the course entered. It will be anything written in english, that we can't parse. So it might make the course untakeable for user, or not matter we don't know
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            return course[8:]
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
        #Returns the points that the course is worth. Can be 7.5 and invalid, as that is half a course. 
        a = self.__cursor.execute("select * from course where subject = ? and courseNumber = ?", (course_subject, course_number))
        list_of_courses = a.fetchall()
        if len(list_of_courses) == 1:
            course = list_of_courses[0]
            return course[3]
        else:
            return 0

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
                return "You need to take: " + pre[0] + " " + pre[1] + " before taking "+  courseName + " " + courseNumber

        a = self.__cursor.execute("select * from restriction where restrictionSubject = ? and restrictionNumber = ?", (courseName, courseNumber))
        res = [(x[2],str(x[3])) for x in a.fetchall()]
        for pre in res:
            if  pre in doing or pre in done_courses:
                return "You cannot take: " + pre[0] + " " + pre[1] + " and " +  courseName + " " + courseNumber

        a = self.__cursor.execute("select * from corequisite where subject = ? and courseNumber = ?;", (courseName, courseNumber))
        res = [(x[0],str(x[1])) for x in a.fetchall()]
        for pre in res:
            if pre not in doing:
                return "You need to take: " + pre[0] + " " + pre[1] + " with taking "+  courseName + " " + courseNumber
        return ""

    def problems_with_timetable(self, timetable):
        new_timetable = []
        probs = []
        for sem in timetable:
            new_timetable.append(sem)
            probs.append([[course[0]+ " " + course[1], self.worst_problems_with_course(course[0],course[1], new_timetable),self.return_isolated_problems_with_course( course[0],  course[1]) ] for course in sem])
        return probs

    def will_graduate_depreciated(self, timetable, majorname):
        done_courses = []
        for semester in timetable:
            for course in semester:
                done_courses.append(course)


        a = self.__cursor.execute("""select majorRequirements.majorID, majorRequirements.majorName, majorRequirements.totalPointsNeeded, "group".subject, "group".courseNumber, course.pointsValue
from majorRequirements
inner join "group"
inner join "course" 
on "group".majorID = majorRequirements.majorID and 
"group".subject = course.subject AND
"group".courseNumber = course.courseNumber AND
majorRequirements.year = 2020;""")
        res = [x for x in a.fetchall()]
        groups = []
        major_groups = {}
        for x in res:
            if x[1] == majorname:
                if x[0] not in major_groups.keys():
                    major_groups.update({x[0]:[x[2], 0]})
                if (x[3],x[4]) in done_courses:
                    major_groups[x[0]][1] = major_groups[x[0]][1] + x[5]

        for x in major_groups:
            if float(major_groups[x][0]) > major_groups[x][1]:
                return False

        probs = self.problems_with_timetable(timetable)
        for x in probs:
            if x[1] != "":
                return False
        return True

    def is_gened(self, couresSubject, courseNumber):
        a = self.__cursor.execute("""select * from  courseScheduleLink""")
        res = [x for x in a.fetchall()]
        for x in res:
            if (x[1] == couresSubject and x[2] == courseNumber):
                return True
        return False

    def def_what_gened_schedule(self, couresSubject, courseNumber):
        a = self.__cursor.execute("""select * from  courseScheduleLink""")
        res = [x for x in a.fetchall()]
        for x in res:
            if (x[1] == couresSubject and x[2] == courseNumber):
                return x[0]
        return "This is not a gen ed"

    def points_from(self,couresSubject, courseNumber ):

        a = self.__cursor.execute("""select course.pointsValue from course WHERE course.subject = ? and course.courseNumber = ?;""", (couresSubject, courseNumber))
        res = [x for x in a.fetchall()]
        for x in res:
            return x[0]
        return "Does not exist"

    def required_courses_to_graduate(self,  major_type, year = "2020", honours = "0"):
        a = self.__cursor.execute("""select group_concat(DISTINCT ( "group".subject || "-" || "group".courseNumber)), sum(course.pointsValue) as "combined points"
        from "group"
        inner join majorGroupLink
        inner join majorRequirements
        inner join "course"
        on "group".groupID = majorGroupLink.groupID AND
        majorRequirements.majorID = "group".majorID AND 
        majorGroupLink.majorID = majorRequirements.majorID AND
        "group".subject = course.subject AND
        "group".courseNumber  = course.courseNumber 
        group by  "group".groupID ,"group".majorID
        having CAST(sum(course.pointsValue) as FLOAT) =  cast(majorGroupLink.pointsRequired as float) and 
        majorRequirements.majorName = ? AND
        majorRequirements.year = ? AND
        majorRequirements.honours = ?;""",(major_type, year,honours))
        res = [x for x in a.fetchall()]
        needed = []
        for x in res:
            for y in x[0].split(","):
                needed.append((y.split("-")[0], y.split("-")[1]))
        return needed

    def required_100_level_courses_to_graduate(self,  major_type, year = "2020", honours = "0"):
        return [x for x in self.required_courses_to_graduate(major_type, year , honours) if x[1][0] == "1"]

    def required_200_level_courses_to_graduate(self,  major_type, year = "2020", honours = "0"):
        return [x for x in self.required_courses_to_graduate(major_type, year , honours) if x[1][0] == "2"]

    def required_300_level_courses_to_graduate(self,  major_type, year = "2020", honours = "0"):
        return [x for x in self.required_courses_to_graduate(major_type, year , honours) if x[1][0] == "3"]

    def required_over_300_level_courses_to_graduate(self,  major_type, year = "2020", honours = "0"):
        return [x for x in self.required_courses_to_graduate(major_type, year , honours) if x[1][0] == "4" or x[1][0] == "5" or x[1][0] == "6" or x[1][0] == "7" or x[1][0] == "8" or x[1][0] == "9"]
        

    def required_courses_in_right_order(self,  major_type, year = "2020", honours = "0"):
        one = self.required_100_level_courses_to_graduate(major_type, year)
        two = self.required_200_level_courses_to_graduate(major_type, year)
        three = self.required_300_level_courses_to_graduate(major_type, year)
        return [one,[],two, [], three]
        
    def might_want_to_take(self,  major_type, timetable, year = "2020", honours = "0"):
        done_courses = []
        for semester in timetable:
            for course in semester:
                done_courses.append(course)

        a = self.__cursor.execute("""select group_concat(DISTINCT ( "group".subject || "-" || "group".courseNumber)),  majorGroupLink.pointsRequired as "combined points"
        from "group"
        inner join majorGroupLink
        inner join majorRequirements
        inner join "course"
        on "group".groupID = majorGroupLink.groupID AND
        majorRequirements.majorID = "group".majorID AND 
        majorGroupLink.majorID = majorRequirements.majorID AND
        "group".subject = course.subject AND
        "group".courseNumber  = course.courseNumber 
        group by  "group".groupID ,"group".majorID
        having CAST(sum(course.pointsValue) as FLOAT) >  cast(majorGroupLink.pointsRequired as float)  AND
        majorRequirements.majorName = ? AND
        majorRequirements.year = ? AND
        majorRequirements.honours = ?;""",(major_type, year, honours))
        res = [x for x in a.fetchall()]
        needed = []
        group = []
        totake = []
        for x in res:
            group.append([x[1],[(z.split("-")[0],z.split("-")[1]) for z in x[0].split(",")]])

        for x in group:
            totalpoints = x[0]
            done_points = 0
            for course in x[1]:
                #print(course[0], course[1],self.points_from(course[0], course[1]), course in done_courses, done_points)
                if course in done_courses:
                    done_points += self.points_from(course[0], course[1])

            if float(done_points) < float(totalpoints):
                totake += x[1]
        return totake

    #This function gives you a list of courses that you need to take some from to graduate. 
    def take_from_these(self,  major_type, timetable, year = "2020", honours = "0"):
        done_courses = []
        for semester in timetable:
            for course in semester:
                done_courses.append(course)

        a = self.__cursor.execute("""select group_concat(DISTINCT ( "group".subject || "-" || "group".courseNumber)),  majorGroupLink.pointsRequired as "combined points"
        from "group"
        inner join majorGroupLink
        inner join majorRequirements
        inner join "course"
        on "group".groupID = majorGroupLink.groupID AND
        majorRequirements.majorID = "group".majorID AND 
        majorGroupLink.majorID = majorRequirements.majorID AND
        "group".subject = course.subject AND
        "group".courseNumber  = course.courseNumber 
        group by  "group".groupID ,"group".majorID
        having CAST(sum(course.pointsValue) as FLOAT) >  cast(majorGroupLink.pointsRequired as float)  AND
        majorRequirements.majorName = ? AND
        majorRequirements.year = ? AND
        majorRequirements.honours = ?;""",(major_type, year, honours))
        res = [x for x in a.fetchall()]
        needed = []
        group = []
        
        for x in res:
            group.append([x[1],[(z.split("-")[0],z.split("-")[1]) for z in x[0].split(",")]])

        totake = []
        temp_group = []
        for x in group:
            totalpoints = x[0]
            done_points = 0
            for course in x[1]:
                print(course[0], course[1],self.points_from(course[0], course[1]), course in done_courses, done_points)
                temp_group.append((course[0], course[1]))
                if course in done_courses:
                    done_points += self.points_from(course[0], course[1])

            if float(done_points) < float(totalpoints):
                totake += temp_group
        return totake

    def reccomended_action(self, major_type, timetable, year = "2020", honours = "0"):
        done_courses = []
        for semester in timetable:
            for course in semester:
                done_courses.append(course)

        #Checks co-req, pre-req and restrictions
        pro = self.problems_with_timetable(timetable)
        for semester in pro:
            for course in semester:
                if course[1] != "":
                    return course[1]

        #Checks required courses
        req_grad = self.required_courses_to_graduate(major_type,"2020")
        if req_grad != []:
            for x in req_grad:
                if x not in done_courses:
                    return "You need to take: " +  x[0] + " " + x[1] + " in order to graduate"

        #CHecks if they are missing poitnfs from some group
        might_take = self.might_want_to_take(  major_type, timetable,"2020")
        if req_grad != []:
            for x in might_take:
                if x not in done_courses:
                    return "You need to get more points from " + ", ".join([x[0]+x[1] for x in might_take]) + " in order to graduate"

        #Checks total points done
        done_points = 0
        for x in done_courses:
            done_points += float(self.return_course_points(x[0],x[1]))
        a = self.__cursor.execute("""select totalPointsNeeded from majorRequirements
        where majorName = ? AND
         year = ? AND
         honours = ?""", (major_type,year, honours))
        dat = a.fetchall()
        if len(dat) > 0:

            if float(done_points) < float(dat[0][0]):
                return "You need to do more points in general"


        

        

        
        a = self.__cursor.execute("""select courseScheduleLink.subject, SUBSTR(courseScheduleLink.courseNumber, 1,
LENGTH(courseScheduleLink.courseNumber)-1) as "CourseNumber",
course.pointsValue
from courseScheduleLink inner join majorRequirements inner join scheduleMajorLink inner JOIN course
on scheduleMajorLink.majorID = majorRequirements.majorID AND
courseScheduleLink.scheduleID = scheduleMajorLink.scheduleID  AND
course.subject = courseScheduleLink.subject AND
course.courseNumber = courseScheduleLink.courseNumber
where 
majorRequirements.majorName = ? AND
majorRequirements.year = ? AND
majorRequirements.honours = ?

union 

select courseScheduleLink.subject, courseScheduleLink.courseNumber as "CourseNumber",
course.pointsValue
from courseScheduleLink inner join majorRequirements inner join scheduleMajorLink inner JOIN course
on scheduleMajorLink.majorID = majorRequirements.majorID AND
courseScheduleLink.scheduleID = scheduleMajorLink.scheduleID  AND
course.subject = courseScheduleLink.subject AND
course.courseNumber = courseScheduleLink.courseNumber
where 
majorRequirements.majorName = ? AND
majorRequirements.year = ? AND
majorRequirements.honours = ?;""", (major_type, year, honours,major_type, year, honours))
        dat = a.fetchall()


        #Checks gen ed points, the right shedules needs to be implemented
        gen_points = 0
        for x in done_courses:
            if (x[0],x[1]) in [(x[0],x[1]) for x in dat]:
                gen_points += float(self.return_course_points(x[0],x[1]))

        a = self.__cursor.execute("""select pointsGenEd from majorRequirements
        where majorName = ? AND
         year = ? AND
         honours = ?""", (major_type,year, honours))
        dat = a.fetchall()
        
        if len(dat) > 0:
            if gen_points < float(dat[0][0]):
                return "You need to do more points gen ed papers"


        return "Looks good"

    def will_graduate(self, timetable, majorname, year = "2020", honours = "0"):
        action = self.reccomended_action(majorname, timetable, year, honours)
        if action == "Looks good":
            return True
        else:
            return False

    def return_all_majorNames(self):
        a = self.__cursor.execute("select DISTINCT majorName from majorRequirements;")
        course = a.fetchall()
        newlist = []
        for x in course:
            newlist.append(x[0])
        return newlist

    def return_all_majorData(self):
        a = self.__cursor.execute("select majorName, honours, level from majorRequirements;")
        course = a.fetchall()
        newlist = []
        for x in course:
            newlist.append(x)
        return newlist


    

a = searchTool()
#print(a.return_all_majorNames())
tim = [[("COMPSCI", "210"),('COMPSCI', '225'),("COMPSCI", "230"),("COMPSCI", "220")],[("COMPSCI", "110"),('COMPSCI', '120'),("ACCTG", "151G")],[("CAREER", "100G"),('COMPSCI', '340'),("COMPSCI", "250")],[("PHIL", "105"),('BIOSCI', '101'),("COMPSCI", "130"),("COMPSCI", "351"),("COMPSCI", "315")]]
tim = [[('CHEM', '110'), ('CHEM', '120')],    [('CHEM', '251'), ('CHEM', '252'), ('CHEM', '253'), ('CHEM', '351')]]
print(a.reccomended_action("chemistry", tim))
