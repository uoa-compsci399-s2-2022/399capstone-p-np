from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import User, Review, make_review, Book
from library.adapters.repository import RepositoryException


# Test that a user can be added to the repository
def test_repository_can_add_a_user(in_memory_repo):
    user = User('arthur', 'Howdy123')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('arthur') is user


# Test that a user can be retrieved from the repository
def test_repository_can_get_a_user(in_memory_repo):
    user = in_memory_repo.get_user('john')
    assert user == User('john', 'Hello123')


# Test that cannot get a user that does not exist from the repository.
def test_repository_does_not_get_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('billy')
    assert user is None


# Test that a book can be added to the repository
def test_repository_can_add_book(in_memory_repo):
    book_id = 30128855
    title = 'Cruelle'
    review_text = 'Such a great book!'
    user_name = 'billy'
    rating = 4

    book_obj = Book(book_id, title)
    print(type(in_memory_repo))
    in_memory_repo.add_book(book_obj)

    assert in_memory_repo.get_book_by_id(30128855) is book_obj


# Tests that a book can be retrieved from the repository from its book id, has the correct title
def test_repository_can_get_book(in_memory_repo):
    book_id = 30128855
    title = 'Cruelle'

    book_obj = Book(book_id, title)
    in_memory_repo.add_book(book_obj)

    book = in_memory_repo.get_book_by_id(30128855)

    # Check that the Book has the expected title.
    assert book.title == 'Cruelle'


# Test that cannot retrieve book that does not exist in repository.
def test_repository_does_not_get_a_non_existent_book(in_memory_repo):
    book = in_memory_repo.get_book_by_id(55)
    assert book is None


# Tests that a review can be added to the repository.
def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('john')

    book_id = 30128855
    title = 'Cruelle'
    review_text = 'Such a great book!'
    rating = 4

    book_obj = Book(book_id, title)
    in_memory_repo.add_book(book_obj)

    book = in_memory_repo.get_book_by_id(30128855)
    review = make_review(review_text, user, book, rating)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_an_book_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('john')

    book_id = 30128855
    title = 'Cruelle'
    review_text = 'Such a great book!'
    rating = 4

    book_obj = Book(book_id, title)
    in_memory_repo.add_book(book_obj)

    review = Review(book_obj, review_text, rating)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Book doesn't refer to the Review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    user = in_memory_repo.get_user('john')

    book_id = 30128855
    title = 'Cruelle'
    review_text = 'Such a great book!'
    user_name = 'billy'
    rating = 4

    book_obj = Book(book_id, title)
    in_memory_repo.add_book(book_obj)

    book = in_memory_repo.get_book_by_id(30128855)
    review = make_review("Great book!", user, book, rating)

    in_memory_repo.add_review(review)

    assert len(in_memory_repo.get_reviews()) == 1
    assert in_memory_repo.get_reviews()[0].user.user_name == 'john'