import abc
from typing import List
from datetime import date, datetime

import csv
from pathlib import Path

from library.domain.model import User, Review, make_review, Book
import library.adapters.jsondatareader as bookdata
import library.domain.model as model
from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

repositoryInstance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


import abc
from typing import List
from datetime import date, datetime

import csv
from pathlib import Path

from library.domain.model import User, Review, make_review, Book
import library.adapters.jsondatareader as bookdata
import library.domain.model as model
from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

repositoryInstance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review is not correctly attached to a User')
        if review.user is None or review not in review.book.reviews:
            raise RepositoryException('Review is not correctly attached to a Book')

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, id: int) -> Book:
        raise NotImplementedError

    def get_book_by_id(self, id):
        raise NotImplementedError


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__users = list()
        self.__reviews = list()
        self.__books = list()
        global repositoryInstance
        if repositoryInstance == None:
            datareader = bookdata.BooksJSONReader("library/adapters/data/comic_books_excerpt.json",
                                                  "library/adapters/data/book_authors_excerpt.json")
            datareader.read_json_files()
            books = datareader.dataset_of_books

            self.database = model.BooksInventory()
            print(books[1])
            for book in books:
                self.database.add_book(book)

            self.currentbookid = 0
            database_instance = self
        self=database_instance

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self.__books[id]
        except KeyError:
            pass

        return book

    def get_book_by_id(self, id):
        for book in self.__books:
            if book.book_id == id:
                return book

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    # -- Not sure where to load from / how to store the reviews --
    def load_from_user_reviews(self):
        rw = open('library/adapters/data/user_reviews.txt', 'r+')
        lines = rw.readlines()
        rw.close()

        for line in lines:
            if line == "\n":
                continue
            print(line)
            self.add_review(Review(line[0]))

    @property
    def data(self):
        return self.database

    @property
    def currentid(self):
        return self.currentbookid

    @currentid.setter
    def currentid(self, value):
        self.currentbookid = value

    def get_database(self):
        return self.database