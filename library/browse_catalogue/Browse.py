from flask import Blueprint

from flask import render_template, redirect, url_for
#import library.adapters.database as database
import library.adapters.repository as repo
browse_blueprint = Blueprint(
    'browse_bp', __name__)
found_book_errors = ""
displayBookIndex = 0



@browse_blueprint.route('/browse', methods=['GET', 'POST'])
def browse():
    global found_book_errors
    global displayBookIndex
    error = found_book_errors
    found_book_errors = ""
    book_library = repo.repositoryInstance.get_database().get_books().values()
    bookList = []
    for item in book_library:
        bookList.append(item)
    NumberOfBooksPerPage = 5
    print(type(book_library))


    data = bookList
    if (len(bookList) > NumberOfBooksPerPage):
        data = []
        count = 0;
        while count < NumberOfBooksPerPage:

            if (len(bookList) > NumberOfBooksPerPage * displayBookIndex + count):
                data.append(bookList[NumberOfBooksPerPage * displayBookIndex + count])
            count += 1



    return render_template(
        'Browse/Browse.html',
        books=data,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        browse=url_for('browse_bp.browse'),
        error=error
    )
    pass

@browse_blueprint.route('/NextBookCatalogue', methods=['GET', 'POST'])
def NextBookCatalogue():
    global displayBookIndex
    data = repo.repositoryInstance.get_database(repo.repositoryInstance).get_books().values()
    if len(data) > (displayBookIndex + 1) * 5:
        displayBookIndex += 1
    return redirect(url_for("browse_bp.browse"))


@browse_blueprint.route('/PreviousBookCatalogue', methods=['GET', 'POST'])
def PreviousBookCatalogue():
    global displayBookIndex
    if 0 != displayBookIndex:
        displayBookIndex -= 1
    return redirect(url_for("browse_bp.browse"))