from datetime import date, datetime
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class AuthorOut(BaseModel):
    id: int
    name: str
    description: str = Field(..., max_length=400)
    email: EmailStr
    books: list
    created_at: datetime


class CategoryOut(BaseModel):
    id: int
    name: str


class BookOut(BaseModel):
    title: str
    resume: str
    summary: str
    price: float
    number_of_pages: int
    isbn: str
    publish_date: date
    category: CategoryOut
