from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model




####################        Depreciated not used anymore but good referance of how it should be done    ####################




# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
publisher_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)

)
author_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('uniqueid', Integer, unique=True, nullable=False)
)
book_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', Integer, nullable=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('publisher', Integer, nullable=True),
    Column('publisher_id', String(255), nullable=False),
    Column('numpages', String(255), nullable=True),
    Column('imageurl', String(255), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('ebook', String(255), nullable=True)

)
reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('review_text', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('rating', Integer, nullable=False)
)
author_book_table = Table(
    'author_books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', ForeignKey('authors.id')),
    Column('book_id', ForeignKey('books.id'))
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
    })
    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__name': publisher_table.c.name,
    })
    mapper(model.Author, author_table, properties={
        '_Author__full_name': author_table.c.name,
        '_Author__unique_id': author_table.c.uniqueid,

    })
    mapper(model.Book, book_table, properties={
        '_Book__id': book_table.c.id,
        '_Book__book_id': book_table.c.book_id,
        '_Book__title': book_table.c.title,
        '_Book__description': book_table.c.description,
        '_Book__publisher_id': book_table.c.publisher_id,
        '_Book__imageurl': book_table.c.imageurl,
        '_Book__release_year': book_table.c.release_year,
        '_Book__ebook': book_table.c.ebook,

        '_Book__authors': relationship(model.Author, secondary=author_book_table),
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__rating': reviews_table.c.rating

    })