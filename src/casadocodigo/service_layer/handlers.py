from sqlalchemy.orm.session import Session

from casadocodigo.service_layer.In import AuthorCreate, BookCreate
from casadocodigo.service_layer import ensure

from casadocodigo.domain.models import Author, Category


def create_author(session: Session, author_create: AuthorCreate):
    author = author_create.to_model()
    session.add(author)
    session.commit()
    return author


def get_author(session: Session, author_id: int) -> Author:
    return session.query(Author).get(author_id)


def create_book(session: Session, author_id: int, book_create: BookCreate):
    ensure.author_exists(session, author_id)
    ensure.category_exists(session, book_create.category_id)

    author = get_author(session, author_id)
    category = get_category(session, book_create.category_id)

    book = book_create.to_model(category)

    author.add_book(book)
    session.commit()
    return book


def get_category(session: Session, category_id: int) -> Category:
    return session.query(Category).get(category_id)
