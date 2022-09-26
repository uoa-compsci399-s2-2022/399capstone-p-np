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

found_book_errors = ""
form_data = None
currentBookValues = ("","","","","","","","","")
currentBook = ""
displayBookIndex = 0;


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



@find_book_blueprint.route('/Displaybook', methods=['GET', 'POST'])
def display_book():
    global currentBookValues
    global currentBook
    values = ''
    if request.method == "POST":
        global displayBookIndex
        displayBookIndex = 0
        req = request.form

        try:
            values = req["MultipleSearchTextBox"].split('+')
            search = SearchEngine.searchTool()
            print(values[0].split()[1]+values[0].split()[0])
            values = search.return_all_course_information(str(values[0].split()[1]).upper(), str(values[0].split()[0]))

        except:
            values = setvalues(req)



        if(values == None):
            return redirect(url_for('find_book_bp.find_book'))

        if isinstance(values[0], list):
            global form_data
            form_data = values
            return redirect(url_for('find_book_bp.display_books'))

    title = values[0] + " " + values[1]
    numberOfPoints = values[3]
    semestersOffered = values[2]
    discription = values[7]
    requirements = values[8]
    error = ""
    if(values == "Error Course not found"):
        title = ""
        numberOfPoints = ""
        semestersOffered = ""
        discription = ""
        requirements = ""
        error = values

    data = getCountryesAndCourses()
    return render_template(
        'Search_for_a_book/Display_book.html',
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),

        title = title,
        numberOfPoints = numberOfPoints,
        semestersOffered = semestersOffered,
        discription = discription,
        requirements=requirements,
        error = error,
        countries = data[1],
        Semester = data[2],
        year = data[3],
        Course = data[4]
    )

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
    print(currentBook)
    print(type(currentBook))
    user.read_a_book(currentBook)

    return redirect(url_for("find_book_bp.display_book"))


def setvalues(req):
    global found_book_errors
    search = SearchEngine.searchTool()
    if req["Course"] != "":
        if ' ' in req["Course"]:
            courseIndex = req["Course"].split(" ")
            CourseData = search.return_all_course_information(courseIndex[0], courseIndex[1])
            print(CourseData)
            return CourseData

        try:
            courseIndex = req["Course"].split(" ")
            courseIndex[1]
        except:
            return "Error Course not found"
        courseIndex = search.return_all_course_information(courseIndex[0])
        print(courseIndex)

        return courseIndex

    if req["Author"] != "":
        found_books = repo.repositoryInstance.data.search_book_by_author(req["Author"])

        if (len(found_books) == 0):
            found_book_errors = "We couldn't find a book that matches your search please try again."
            return None
        if (len(found_books) == 1):
            return display_one_book(found_books[0])
        return found_books

    if req["Publisher"] != "":
        found_books = repo.repositoryInstance.data.search_book_by_publishers(req["Publisher"])

        if (len(found_books) == 0):
            found_book_errors = "We couldn't find a book that matches your search please try again."
            return None
        if (len(found_books) == 1):
            return display_one_book(found_books[0])
        return found_books

    if req["Release_year"] != "":
        try:
            year = int(req["Release_year"])
        except:
            found_book_errors = "Please enter a number."
            return None
        found_books = repo.repositoryInstance.data.search_book_by_release_year(year)

        if (len(found_books) == 0):
            found_book_errors = "We couldn't find a book that matches your search please try again."
            return None
        if (len(found_books) == 1):
            return display_one_book(found_books[0])
        return found_books

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

def getCountryesAndCourses():

    search = SearchEngine.searchTool()
    global found_book_errors
    countries = str(search.return_all_courses())
    #print(countries)
    countries = countries[3:len(countries)-3]
    countries = re.sub(r"[\'\,]", '', countries)
    countries = countries.replace("', ' ", '')
    #print(countries)
    #print(countries)
    #countries = "pears"
    error = found_book_errors
    found_book_errors = ""
    semester = "1, 2"
    year = "2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025"
    count = 0
    course = ""
    falseflag = False
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