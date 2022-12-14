import sqlite3

conn = sqlite3.connect('399courses.db')

print("Opened database successfully")

#the DATABASE does not currently hold this information so it has been hardcoded 
Major_Requirements_Subject_Names = [COMPSCI,COMPSCI,COMPSCI,COMPSCI,COMPSCI,COMPSCI,COMPSCI]
Major_Requirements_Subject_Numbers = [110,120,130,210,220,230,399]
200_level_Points = 180
300_Level_points = 75

def major_requirments():
    a = self.__cursor.execute("""select majorRequirements.majorID, majorRequirements.majorName, majorRequirements.totalPointsNeeded, "group".subject, "group".courseNumber, course.pointsValue from majorRequirements inner join "group" inner join "course" 
    on "group".majorID = majorRequirements.majorID and 
    "group".subject = course.subject AND
    "group".courseNumber = course.courseNumber;""")
        res = [x for x in a.fetchall()]
        groups = []
        major_groups = {}
        for x in res:
            if x[1] == majorname:
                if x[0] not in major_groups.keys():
                    major_groups.update({x[0]: [x[2], 0]})
                if (x[3], x[4]) in done_courses:
                    major_groups[x[0]][1] = major_groups[x[0]][1] + x[5]

        for x in major_groups:
            print(major_groups[x][0], major_groups[x][1])
            if float(major_groups[x][0]) > major_groups[x][1]:
                return False

        probs = self.problems_with_timetable(timetable)
        for x in probs:
            if x[1] != "":
                return False
        return True


def meets_graduation_requirements(Faculty,Major,Couse_Subject,Course_Number):
    Number_of_papers_taken=len(Course_Subject) #Number of Papers in the Degree Planner
    Total_p=conn.execute("SELECT totalPointsNeeded from majorRequirements where majorName = ?", (Major))
    Total_points=Total_p.fetchall() # this is the total points need for their Major

    points = 0   #used to calculate Total Points earned
    points_above_200 = 0 #used to calculate the points earned that are above 200 level
    points_above_300 = 0 #used to calculate the points earned that are above 200 level
    Major_Check = 0  #this is used to Check GenED requirements
    Combined_name_of_subject = list()  #this combines the Subject Name and Number into a single string
    List_of_MajorType = list()  #this lists the related Faculty each Paper is from

  

    for i in range(0,Number_of_papers_taken):
        Combined_name_of_subject[i]=Couse_Subject[i]+Course_Number[i] # Combines the two lists together

        a = cursor.execute("select pointsValue from course where subject = ? and courseNumber = ?", (Couse_Subject[i],Course_Number[i]))
        p = int(a.fetchall())
        points=points+p
        if(Course_Number[i]>200):#adds all the papers which are 200 level or above to a list
            points_above_200=points_above_200+p
        if (Course_Number[i] > 200): #adds all the papers which are 300 level or above to a list
            points_above_300 = points_above_300 + p
        b=cursor.execute("select majorType from course where subject = ? and courseNumber = ?", (Couse_Subject[i],Course_Number[i]))
        q=b.fetchall()
        List_of_MajorType.append(q)

    #this sections check that the user is completing enough points overall as well above 200 level and above 300 level
    if(points<Total_points): #checks if the User has enough TOTAL points
        print("Not enough points to Graduate")
        return 0
    if (points < 200_level_Points):  # checks if the User has enough TOTAL points
        print("Not enough points from papers 200 level or greater to Graduate")
        return 0
    if (points < 300_level_Points):  # checks if the User has enough TOTAL points
        print("Not enough points from papers 300 level or greater to Graduate")
        return 0



    #this section checks that the user meets the GenED requirement by checking that two paper is from a different MajorType
    for m in List_of_MajorType:
        if(m != Faculty):
            Major_Check=Major_Check+1
    if(Major_Check<2):#Checks that the user is enrolled in 2 papers from a different Faculty 
        print("The user is not enrol in a GenED subject from a different Faculty to ?", (Major_Type))
        return 0
    if(Major_Check>2):#checks if more than 30 points are from outside their Faculty
        print("The user is enrolled in too many papers from facultys outside of ?", (Major_Type))
        return 0

    #this section check that the user is taking all the requirement papers within the degree
    Combined_name_of_requirements=list()
    for i in range(0,len(Major_Requirements_Subject_Names):
        Combined_name_of_requirements[i]=Major_Requirements_Subject_Names[i]+Major_Requirements_Subject_Names[i] # Combines the two lists together
    results=all(elem in Combined_name_of_subject for elem in Combined_name_of_requirements)
    if(results !=True):
        print("The user is not enrolled in all the requirements of their degree")
        return 0


#this section checks that the user does not have any restrictions in their degree

    for i in range(Number_of_papers_taken):
        for j in range(Number_of_papers_taken):
            if(i !=0):
                no_restrictions=Check_if_restrictions(Course_Subject[i],Course_Number[i],Course_Subject[j],Course_Number[j])
                if(no_restrictions==0):
                    print("User is taking two papers that are restrictions of each other")
                    return 0
                   
 #call the function that checks Major Requirement Groups:
    req=major_requirments()
    if(req==false):
        return 0

#if all other tests have been passed, return 1 as all requirments are meet
    return 1
