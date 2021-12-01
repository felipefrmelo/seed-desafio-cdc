
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session
from casadocodigo.author.handlers import create_author, create_book
from casadocodigo.author.test_author import author_id

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from . import dtos, model
from ..dependencies import get_db

app = APIRouter(prefix="/author", tags=["author"])


@app.post("/", response_model=dtos.AuthorOut, status_code=201)
def create_author_endpoint(user: dtos.AuthorCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, model.Author, "email", user.email)

    return create_author(db, user)


@app.post("/{author_id}/book",  status_code=201, response_model=dtos.BookOut)
def create_book_endpoint(
        author_id: int,
        book: dtos.BookCreate,
        db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        db, model.Book, "isbn", book.isbn)

    return create_book(db, author_id, book)
