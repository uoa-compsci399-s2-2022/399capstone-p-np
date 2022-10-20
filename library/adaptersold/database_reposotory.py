from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, Author, Publisher
from library.adapters.repository import AbstractRepository

#testing push to main

####################        Depreciated not used anymore but good referance of how it should be done    ####################
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository():

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str):
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            return None
        return user

    def add_book(self, book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book_by_title(self, title: str):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__title == title).one()
        except NoResultFound:
            return None
        return book

    def get_book_by_year(self, year: str):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__release_year == year).all()
        except NoResultFound:
            return None
        return book

    def get_book_by_author(self, year: str):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter().all()
        except NoResultFound:
            return None
        return book

    def get_book_by_publisher(self, name: str):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__publisher_id == name).all()
        except NoResultFound:
            return None
        return book

    def get_book_by_id(self, name: str):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == name).one()
        except NoResultFound:
            return None
        return book

    def add_publisher(self, publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def get_publisher(self, name: str):
        publisher = None
        try:
            publisher = self._session_cm.session.query(Publisher).filter(Publisher._Publisher__name == name).one()
        except NoResultFound:
            return None
        return publisher

    def add_author(self, author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_author(self, name: str):
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._Author__full_name == name).one()

        except NoResultFound:
            return None
        return author

    def get_all_books(self):
        try:
            publisher = self._session_cm.session.query(Book).filter().all()
        except NoResultFound:
            return None
        return publisher

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()