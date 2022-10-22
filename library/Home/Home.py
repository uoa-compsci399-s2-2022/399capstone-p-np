from flask import Blueprint, render_template, url_for

from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

import library.adapters.DbFunctions as SearchEngine
import library.adaptersold.jsondatareader as bookdata
import library.domain.model as model
import library.find_book.find_book as findbook
import datetime
import re
import csv
import os

home_blueprint = Blueprint(
    'home_bp', __name__
)
semesters = []

MagorSelected = ""

@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    global semesters
    global MagorSelected
    WorkingDegree = []
    Databaseaccess = SearchEngine.searchTool()
    Magor = str(Databaseaccess.return_all_majorNames())
    Magor = Magor[2:len(Magor) - 2]
    Magor = re.sub(r"[\'\,]", '', Magor)
    Magor = Magor.replace("', ' ", '')
    UpdateDegreePlanner()

    reqFirstYearZacTest = Databaseaccess.required_100_level_courses_to_graduate("computer-science")

    if request.method == "POST":
        req = request.form
        destroy = False


        try:
            formOutput = req["MultipleSearchTextBox"]
        except:
            try:
                MagorSelected = req["Courses"]
                autofillCoursesWithRequirements(MagorSelected)


                CleanSemesterData = StripSemestersOfTitleFluff(semesters)
                RecomendedAction = [Databaseaccess.reccomended_action(MagorSelected, CleanSemesterData)]

                if RecomendedAction == ["Your course will allow you to graduate"]:
                    RecomendedAction = []
                    WorkingDegree = ["Your degree will allow you to graduate"]
                return render_template(
                    'Home_Page.html',
                    semesters=semesters,
                    books=bookdata.reader_instance,
                    home_url=url_for('home_bp.home'),
                    find_book=url_for('find_book_bp.find_book'),
                    Course=Magor,
                    reqFirstYearZacTest=reqFirstYearZacTest,
                    RecomendedAction = RecomendedAction,
                    WorkingDegree = WorkingDegree
                    # user = ("Welcome " + str(session['user_name']))
                )
            except:
                formOutput = req["DESTROY"]
                destroy = True


        for item in semesters:
            if item[0] == formOutput.split("+")[1]:
                search = SearchEngine.searchTool()
                searchResult = search.return_all_course_information(formOutput.split("+")[0].split(" ")[0].upper(), formOutput.split("+")[0].split(" ")[1])
                print(searchResult)
                print(formOutput.split("+")[0].split(" ")[1].upper() + formOutput.split("+")[0].split(" ")[0])
                CourseName = formOutput.split("+")[0]
                CourseName = CourseName.split(" ")[0] + " " + CourseName.split(" ")[1]
                if destroy:
                    for course in item[1:]:
                        if course[0] == CourseName:
                            item.remove(course)
                            break


                else:
                    item.append([CourseName, searchResult[8]])

    RecomendedAction = []
    if MagorSelected != "":
        CleanSemesterData = StripSemestersOfTitleFluff(semesters)
        RecomendedAction = [Databaseaccess.reccomended_action(MagorSelected, CleanSemesterData)]

    #totalNumberOfCourses = 0
    #for item in semesters:
        #totalNumberOfCourses += len(item)-1

    if RecomendedAction == ["Your course will allow you to graduate"]:

        RecomendedAction = []
        WorkingDegree = ["Your degree will allow you to graduate"]
        #else:
            #RecomendedAction = ["You need to take at least 24 pappers to graduate"]
            #WorkingDegree = []

    return render_template(
        'Home_Page.html',
        semesters=semesters,
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        Course = Magor,
        reqFirstYearZacTest = reqFirstYearZacTest,
        RecomendedAction = RecomendedAction,
        WorkingDegree = WorkingDegree
        #user = ("Welcome " + str(session['user_name']))
    )



def TransferSemestersToZacesters(data):
    newdata =[]
    c = 0
    for item in data:
        newdata.append([])
        newitem = item[1:]

        for course in newitem:
            newdata[c].append((course[0].split(" ")[1], course[0].split(" ")[0]))
        c+=1
    return newdata

def autofillCoursesWithRequirements(values):
    global semesters
    DataBaseAccess = SearchEngine.searchTool()
    year1 = DataBaseAccess.required_100_level_courses_to_graduate(values)
    year2 = DataBaseAccess.required_200_level_courses_to_graduate(values)
    year3 = DataBaseAccess.required_300_level_courses_to_graduate(values)

    semesters = []
    today = datetime.date.today()
    DisplayYear = int(today.strftime("%Y"))
    addSemesterToCourse(DataBaseAccess, year1, DisplayYear)
    addSemesterToCourse(DataBaseAccess, year2, DisplayYear + 1)
    addSemesterToCourse(DataBaseAccess, year3, DisplayYear + 2)

    UpdateDegreePlanner()


def addSemesterToCourse(DataBaseAccess, year, DisplayYear):
    courses = [str(DisplayYear)]
    for item in year:
        courseData = DataBaseAccess.return_all_course_information(item[0], item[1])
        courses.append([courseData[0] + " " + courseData[1], courseData[8]])
    semesters.append(courses)
    UpdateDegreePlanner()

def StripSemestersOfTitleFluff(semesters):
    cleanSemesters = []
    for item in semesters:
        semester = []
        for course in item[1:]:
            semester.append((course[0].split(" ")[0], course[0].split(" ")[1]))
        cleanSemesters.append(semester)
    UpdateDegreePlanner()
    return cleanSemesters

def UpdateDegreePlanner():
    ROOT_DIR = os.path.abspath(os.curdir)

    f = open(ROOT_DIR + '\\library\\static\\DegreePlanner.txt', 'w+')
    f.write(MagorSelected + "\n")
    for year in semesters:
        f.write(year[0] + "\n")
        bucket = ""
        for course in year:
            if course[0][0] == "2":
                continue
            bucket+= " " + course[0]
        f.write(bucket + "\n")
    f.close()