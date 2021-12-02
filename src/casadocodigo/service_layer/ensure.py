
from abc import ABCMeta, abstractmethod
from typing_extensions import NotRequired
from sqlalchemy.orm.session import Session
from abc import abstractmethod
from typing import List, Optional, TypedDict

from casadocodigo.domain.models import Author, Category
from casadocodigo.service_layer.errors import AuthorNotFound, CategoryNotFound


def author_exists(session: Session, author_id: int):
    author = session.query(Author).get(author_id)
    if author is None:
        raise AuthorNotFound()


def category_exists(session: Session, category_id: int):
    category = session.query(Category).get(category_id)
    if category is None:
        raise CategoryNotFound()
