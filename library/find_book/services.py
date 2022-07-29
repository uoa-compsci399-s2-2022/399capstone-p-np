from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import User, make_review, Book, Review


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(book, review_text: str, user_name: str, repo: AbstractRepository, rating):

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(review_text, user, book, rating)

    repo.add_review(review)


def get_reviews_for_books(book_id, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'article_id': review.article.id,
        'comment_text': review.comment,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
