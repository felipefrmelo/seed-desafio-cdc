
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session
from casadocodigo.service_layer.In import AuthorCreate, BookCreate
from casadocodigo.service_layer.Out import AuthorOut, BookOut
from casadocodigo.service_layer.handlers import create_author, create_book

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from ..dependencies import get_db


from casadocodigo.domain.models import Author, Book


app = APIRouter(prefix="/author", tags=["author"])


@app.post("/", response_model=AuthorOut, status_code=201)
def create_author_endpoint(user: AuthorCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, Author, "email", user.email)

    return create_author(db, user)


@app.post("/{author_id}/book",  status_code=201, response_model=BookOut)
def create_book_endpoint(author_id: int, book: BookCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, Book, "isbn", book.isbn)

    return create_book(db, author_id, book)
