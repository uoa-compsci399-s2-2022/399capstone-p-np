from better_profanity import profanity
from flask import Blueprint, render_template, url_for

from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.jsondatareader as bookdata

from library.authentication.authentication import login_required
import library.adapters.repository as repo
import library.find_book.services as services
import library.authentication.services as authServices

find_book_blueprint = Blueprint(
    'find_book_bp', __name__
)

found_book_errors = ""
form_data = None
currentBookValues = ("","","","","","","","","")
currentBook = None
displayBookIndex = 0;


@find_book_blueprint.route('/search', methods=['GET', 'POST'])
def find_book():

    global found_book_errors

    error = found_book_errors
    found_book_errors = ""
    return render_template(
        'Search_for_a_book/find_book.html',
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        error=error,
        #user=("Welcome " + str(session['user_name']))
    )
    pass


@find_book_blueprint.route('/Displaybook', methods=['GET', 'POST'])
def display_book():
    global currentBookValues
    global currentBook
    currentBook = repo.repositoryInstance
    if request.method == "POST":
        global displayBookIndex
        displayBookIndex = 0
        req = request.form


        values = None
        try:
            found_book = repo.repositoryInstance.data.search_book_by_id(req["MultipleSearchTextBox"])
            values = display_one_book(found_book)
        except:
            values = setvalues(req)

        if(values == None):
            return redirect(url_for('find_book_bp.find_book'))

        if type(values) != tuple:
            global form_data
            form_data = values
            return redirect(url_for('find_book_bp.display_books'))

        currentBookValues = values



    return render_template(
        'Search_for_a_book/Display_book.html',
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),

        Title=currentBookValues[0],
        Author=currentBookValues[1],
        Discription=currentBookValues[2],
        Image=currentBookValues[3],
        Publisher=currentBookValues[4],
        Published_Date=currentBookValues[5],
        Ebook=currentBookValues[6],
        Reviews=currentBookValues[7],
        book=currentBook
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

    if req["Title"] != "":
        found_book = repo.repositoryInstance.data.search_book_by_title(req["Title"])
        if (found_book == None):
            found_book_errors = "We couldn't find a book that matches your search please try again."
            return None
        return display_one_book(found_book)

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
@login_required
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

