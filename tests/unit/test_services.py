from datetime import date

import pytest

from library.authentication.services import AuthenticationException
from library.find_book import services as find_book_services
from library.authentication import services as auth_services
from library.find_book.services import NonExistentBookException

from library.domain.model import Book


# Tests adding a new user.
def test_adding_user(in_memory_repo):
    new_user_name = 'joey'
    new_password = 'Howdy123'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


# Tests adding an existing username
def test_cannot_add_existing_username(in_memory_repo):
    user_name = 'john'
    password = 'Hello123'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


# Tests adding a new user with valid credentials
def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'arthur'
    new_password = 'Yeehaw246'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


# Tests adding new user with invalid credentials
def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


###########################################################################################




def test_cannot_add_review_by_unknown_user(in_memory_repo):
    book_id = 30128855
    title = 'Cruelle'
    review_text = 'Such a great book!'
    user_name = 'billy'
    rating = 4

    book_obj = Book(book_id, title)

    # Call the service layer to attempt to add the comment.
    with pytest.raises(find_book_services.UnknownUserException):
        find_book_services.add_review(book_obj, review_text, user_name, in_memory_repo, rating)


# Tests if we can get a book from the repo as dictionary
def test_can_get_book(in_memory_repo):
    book_id = 30128855
    title = 'Cruelle'

    book_obj = Book(book_id, title)
    find_book_services.add_book(book_obj, in_memory_repo)

    book_as_dict = find_book_services.get_book(book_id, in_memory_repo)

    assert book_as_dict['id'] == 30128855
    assert book_as_dict['title'] == 'Cruelle'


# Tests that we cannot get a book with a non-existent id.
def test_cannot_get_book_with_non_existent_id(in_memory_repo):
    book_id = 5

    # Call the service layer to attempt to retrieve the Book.
    with pytest.raises(find_book_services.NonExistentBookException):
        find_book_services.get_book(book_id, in_memory_repo)




# Tests getting reviews for a book that does not exist.
def test_get_reviews_for_non_existent_book(in_memory_repo):
    with pytest.raises(NonExistentBookException):
        reviews_as_dict = find_book_services.get_reviews_for_books(7, in_memory_repo)


# Tests getting book reviews for a book with no reviews.
def test_get_reviews_for_book_without_reviews(in_memory_repo):
    book_id = 30128855
    title = 'Cruelle'

    book_obj = Book(book_id, title)
    find_book_services.add_book(book_obj, in_memory_repo)

    reviews_as_dict = find_book_services.get_reviews_for_books(30128855, in_memory_repo)
    assert len(reviews_as_dict) == 0
