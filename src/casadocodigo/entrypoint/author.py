
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session
from casadocodigo.service_layer.handlers import create_author, create_book

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from ..dependencies import get_db

from datetime import date, datetime
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from .category import CategoryOut
from casadocodigo.domain.models import Author, Book, Category


app = APIRouter(prefix="/author", tags=["author"])


class BaseAuthor(BaseModel):
    name: str
    description: str = Field(
        title="The description of the item", max_length=400)
    email: EmailStr


class AuthorCreate(BaseAuthor):

    def to_model(self):
        return Author(name=self.name, description=self.description, email=self.email)


class AuthorOut(BaseAuthor):
    id: int
    books: list
    created_at: datetime


class BookCreate(BaseModel):
    title: str
    resume: str
    summary: str = Field(
        title="The description of the item", max_length=500)
    price: float = Field(..., ge=20)
    number_of_pages: int
    isbn: str
    publish_date: date
    category_id: int

    def to_model(self, category: Category):
        return Book(
            title=self.title,
            resume=self.resume,
            summary=self.summary,
            price=self.price,
            number_of_pages=self.number_of_pages,
            isbn=self.isbn,
            publish_date=self.publish_date,
            category=category
        )


class BookOut(BaseModel):
    title: str
    resume: str
    summary: str
    price: float
    number_of_pages: int
    isbn: str
    publish_date: date
    category: CategoryOut


@app.post("/", response_model=AuthorOut, status_code=201)
def create_author_endpoint(user: AuthorCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, Author, "email", user.email)

    return create_author(db, user)


@app.post("/{author_id}/book",  status_code=201, response_model=BookOut)
def create_book_endpoint(
        author_id: int,
        book: BookCreate,
        db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        db, Book, "isbn", book.isbn)

    return create_book(db, author_id, book)
