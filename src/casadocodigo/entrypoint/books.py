
from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session
from casadocodigo.service_layer.Out import BookOutList, BookOutDetail
from casadocodigo.service_layer.errors import BookNotFound
from ..dependencies import get_db
from casadocodigo.domain.models import Book, Author


app = APIRouter(prefix="/books", tags=["books"])


@app.get("/", response_model=List[BookOutList], status_code=200)
def get_books_entrypoint(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/{title}", response_model=BookOutDetail, status_code=200)
def get_book_entrypoint(title: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(title=title).first()
    if book is None:
        raise BookNotFound()
    return BookOutDetail.from_orm(book)
