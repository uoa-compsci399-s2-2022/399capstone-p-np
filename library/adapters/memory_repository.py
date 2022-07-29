import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash
from library.adapters import repository as repo
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import User, Review, make_review, Book
import library.adapters.jsondatareader as bookdata
import library.domain.model as model
import os

class MemoryRepository():
    def __init__(self):
        self.__users = list()
        self.__reviews = list()
        self.__books = list()
        if repo.repo_instance == None:
            path = os.getcwd()
            path.replace("\\","/")
            print (path[:len(path)-10])
            datareader = bookdata.BooksJSONReader(path[:len(path)-10] + "/library/adapters/data/comic_books_excerpt.json",
                                                  path[:len(path)-10] + "/library/adapters/data/book_authors_excerpt.json")

            datareader.read_json_files()
            books = datareader.dataset_of_books

            self.database = model.BooksInventory()
            for book in books:
                self.database.add_book(book)

            self.currentbookid = 0
            repo.repo_instance = self
        self=repo.repo_instance

    def add_user(self, user: User):
        self.__users.append(user)

    def add_book(self, book):
        self.__books.append(book)

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


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user

    return users


def populate(data_path: Path, repo: MemoryRepository):
    # Load users into the repository.
    users = load_users(data_path, repo)






