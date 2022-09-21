import sqlite3

conn = sqlite3.connect('399courses.db')

print("Opened database successfully")

cursor = conn.execute("SELECT subject, courseNumber, MajorType, pointsValue, GPAreq, level,  approvalNeeded, description, problematicPreReqs, problematicRestrictions, problematicCoReqs, problematicOther FROM course")
cursor = conn.execute("SELECT restrictionSubject, restrictionNumber, subject, courseNumber FROM restriction")



##Lists all available papers within a major type at a certain level
def list_papers_major_type_level(MajorType,level):
    a = cursor.execute("select * from course where MajorType = ? and level = ?",(MajorType,level))
    list_of_courses = a.fetchall()
    return list_of_courses

#Checks if a paper is a restriction of another paper
def Check_if_restrictions(subject_A,courseNumber_A,subject_B,courseNumber_B):
    a=conn.execute("Select restrictionSubject, restrictionNumber from restriction where subject=? and courseNumber=?",(subject_A, courseNumber_A))
    a_rest=a.fetchall()
    for row in a_rest:
        if(row[0]==subject_B and  row[0]==courseNumber_B):
            print(subject_B+''+courseNumber_B+"is a restriction")
            return
    return 1

