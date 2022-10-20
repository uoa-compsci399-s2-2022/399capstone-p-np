from better_profanity import profanity
from flask import Blueprint, render_template, url_for

from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import library.Home.Home as home
import library.adapters.DbFunctions as SearchEngine
import library.adaptersold.jsondatareader as bookdata
import json
import library.adaptersold.repository as repo
import re
find_book_blueprint = Blueprint(
    'find_book_bp', __name__
)


#list of global variables that will persist between page loading
found_book_errors = ""
form_data = None
currentBookValues = ("","","","","","","","","")
currentBook = ""
displayBookIndex = 0;
Coordinates = ""

#basic search page that doesn't show any additional information than the search bar
@find_book_blueprint.route('/search', methods=['GET', 'POST'])
def find_book():
    #print(course)
    #print(countries)
    data = getCountryesAndCourses()
    return render_template(
        'Search_for_a_book/find_book.html',
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        error=data[0],
        countries=data[1],
        Semester=data[2],
        year=data[3],
        Course=data[4]
        #user=("Welcome " + str(session['user_name']))
    )
    pass


#Displays the search bar and handles inputs like a search and the add remove buttons
@find_book_blueprint.route('/Displaybook', methods=['GET', 'POST'])
def display_book():
    global found_book_errors
    found_book_errors = ""
    global currentBookValues
    global currentBook
    values = ''
    global Coordinates

    #if a button took us here (Add remove search or home page course click)
    if request.method == "POST":
        global displayBookIndex
        displayBookIndex = 0
        req = request.form

        try:
            #we hit submit on the search bar
            values = req["MultipleSearchTextBox"].split('+')
            search = SearchEngine.searchTool()
            Coordinates = values[2]
            values = [search.return_all_course_information(str(values[0].split()[0]).upper(), str(values[0].split()[1]))]

        except:
            #we clicked on the plus on the home screen
            try:
                values = req["PlusBox"]
                Coordinates = values
                values = None
            except:
                #we clicked on a course on the home screen
                values = setvalues(req)


        #if we didn't get passed a value don't do anything
        if(values == None):
            return redirect(url_for('find_book_bp.find_book'))

        #if there are multiple courses returned display multiple courses
        if isinstance(values[0], list):
            global form_data
            form_data = values
            return redirect(url_for('find_book_bp.display_books'))

    #Sets coordinates in the semester array to be displayed on the home screen
    if Coordinates == "":
        Coordinates = home.semesters[0][0]

    print(values)

    #converts values to an array that is then able to be looped over in java
    record = getCourseArray(values)

    data = getCountryesAndCourses()
    return render_template(
        'Search_for_a_book/Display_book.html',
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),

        reviews = record,

        countries = data[1],
        Semester = data[2],
        year = data[3],
        Course = data[4],

        found_book_errors = found_book_errors
    )

#returns an array of courses that can be looped over in java in the home page
def getCourseArray(item):
    bucket = []
    print(item)
    for values in item:
        title = values[0] + " " + values[1]
        numberOfPoints = values[3]
        semestersOffered = values[2]
        discription = values[7]
        requirements = values[8]
        error = ""
        if (values == "Error Course not found"):
            title = ""
            numberOfPoints = ""
            semestersOffered = ""
            discription = ""
            requirements = ""
            error = values


        bucket.append([title, semestersOffered, numberOfPoints, discription, requirements, Coordinates])
    print(bucket[0])
    return bucket


@find_book_blueprint.route('/Displaybooks', methods=['GET', 'POST'])
def display_books():
    data = form_data
    if (len(form_data) > 3):
        data = []
        if(len(form_data) > 3 * displayBookIndex):
            data.append(form_data[3*displayBookIndex])
        if (len(form_data) > 3 * displayBookIndex + 1):
            data.append(form_data[3 * displayBookIndex + 1])
        if (len(form_data) > 3 * displayBookIndex + 2):
            data.append(form_data[3 * displayBookIndex + 2])

    return render_template(
        'Search_for_a_book/Display_books.html',
        books=data
    )

@find_book_blueprint.route('/NextBook', methods=['GET', 'POST'])
def NextBook():
    global displayBookIndex
    if len(form_data) > (displayBookIndex + 1) * 3:
        displayBookIndex += 1
    return redirect(url_for("find_book_bp.display_books"))


@find_book_blueprint.route('/PreviousBook', methods=['GET', 'POST'])
def PreviousBook():
    global displayBookIndex
    if 0 != displayBookIndex:
        displayBookIndex -= 1
    return redirect(url_for("find_book_bp.display_books"))


@find_book_blueprint.route('/addbooktoread', methods=['GET', 'POST'])
def addBook():
    user=None
    user = authServices.get_whole_user(session['user_name'], repo.repo_instance)
    user.read_a_book(currentBook)

    return redirect(url_for("find_book_bp.display_book"))

#calls functions that preform the search algorithm
def setvalues(req):
    global found_book_errors
    search = SearchEngine.searchTool()



    #if the faculty search is filled and they didn't enter a spesific course return all courses that match
    if req["Degree"] != "" and str(req["Course"].strip()) in str(req["Degree"]):
        CoruseData = []
        print(req["Degree"] + "data")
        courseInfo = search.return_all_courses()
        for item in courseInfo:
            if item[0] == req["Degree"]:
                CoruseData.append(search.return_all_course_information(item[0], item[1]))
        print(CoruseData)
        return CoruseData

    #if the course search is for a spesific course just return that one
    if req["Course"] != "":
        if ' ' in req["Course"]:
            courseIndex = req["Course"].split(" ")
            CourseData = search.return_all_course_information(courseIndex[0], courseIndex[1])
            print(CourseData)
            return [CourseData]

        try:
            courseIndex = req["Course"].split(" ")
            courseIndex[1]
        except:
            return "Error Course not found"
        courseIndex = search.return_all_course_information(courseIndex[0])

        return [courseIndex]




    found_book_errors = "Please enter a value."
    return None


def display_one_book(found_book):

    strv = ""
    for author in found_book.authors:
        strv += author.full_name + ", "
    if strv != "":
        strv = strv[:len(strv) - 2]

    ebook = "No Ebook available"
    if found_book.ebook:
        ebook = "Ebook is available"

    relece_year = found_book.release_year
    if found_book.release_year == None:
        relece_year = "N/A"

    publisher = found_book.publisher.name
    if found_book.publisher.name == None:
        publisher = "N/A"

    global currentBook
    currentBook=found_book

    reviews = 'N/A'
    average = 0;
    count = 0
    for item in found_book.reviews:
        average+=item.rating
        count+=1
    if(count != 0):
        reviews = str(average / count)

    return (found_book.title, strv, found_book.description, found_book.Image, publisher, relece_year, ebook, reviews)


@find_book_blueprint.route('/review', methods=['GET', 'POST'])
def review_book():
    global currentBook
    user_name = session['user_name']
    form = ReviewForm()
    book_id = repo.repositoryInstance.data.find_book_key(currentBook)

    if form.validate_on_submit():
        ratingerror = ""
        if request.form["Rating"] == "":
            ratingerror = "Enter a rating."
        try:
            services.add_review(currentBook, form.review.data, user_name, repo.repositoryInstance, int(request.form["Rating"]))
        except(ValueError):
            ratingerror = "Enter a rating from 1 to 5."
        # except:
        #     ratingerror="You must be logged in"

        if ratingerror != '':
            return render_template(
                'Search_for_a_book/review_book.html',
                title='Edit book',
                book=currentBook,
                form=form,
                handler_url=url_for('find_book_bp.review_book'),
                books=bookdata.reader_instance,
                ratingerror=ratingerror
            )

        return redirect(url_for('find_book_bp.find_book', view_reviews_for=book_id))

    if request.method == 'GET':
        form.book_id.data = book_id

    return render_template(
        'Search_for_a_book/review_book.html',
        title='Edit book',
        book=currentBook,
        form=form,
        handler_url=url_for('find_book_bp.review_book'),
        books=bookdata.reader_instance
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Must NOT contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must NOT contain profanity')])
    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')

#this converts the sql return value into the format that the home page needs to return the data and splits the name
#into the faculty and the course number due to the way that we have addressed it
def getCountryesAndCourses():
    # it cleans the array returned as a string into a string that can then be displayed directly on the screen
    search = SearchEngine.searchTool()
    global found_book_errors
    countries = str(search.return_all_courses())
    #print(countries)
    countries = countries[3:len(countries)-3]
    countries = re.sub(r"[\'\,]", '', countries)
    countries = countries.replace("', ' ", '')

    error = found_book_errors
    found_book_errors = ""
    semester = "1, 2"
    year = "2020, 2021, 2022, 2023"
    count = 0
    course = ""
    falseflag = False

    #removes spaces from every second word
    while count < len(countries):
        if countries[count] == " ":
            falseflag = not falseflag
        if falseflag:
            count+=1
            continue
        course = course + countries[count]
        count+=1
    course = course.split(" (")
    courseArray = []
    for item in course:
        if item not in courseArray:
            courseArray.append(item)
    courseArray = str(courseArray)
    courseArray = courseArray[2:len(courseArray) - 2]
    courseArray = re.sub(r"[\'\,]", '', courseArray)
    courseArray = courseArray.replace("', ' ", '')









    return (error, countries, semester, year, courseArray)
