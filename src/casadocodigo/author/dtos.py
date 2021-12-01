
from datetime import date, datetime
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from . import model
from ..entrypoint.category import CategoryOut

class BaseAuthor(BaseModel):
    name: str
    description: str = Field(
        title="The description of the item", max_length=400)
    email: EmailStr


class AuthorCreate(BaseAuthor):

    def to_model(self):
        return model.Author(name=self.name, description=self.description, email=self.email)


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

    def to_model(self, category: model.Category):
        return model.Book(
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
