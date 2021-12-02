from datetime import date, datetime
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class AuthorOut(BaseModel):
    id: int
    name: str
    description: str
    email: EmailStr
    books: list
    created_at: datetime


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    title: str
    resume: str
    summary: str
    price: float
    number_of_pages: int
    isbn: str
    publish_date: date
    category: CategoryOut


class BookOutList(BaseModel):
    isbn: str
    title: str


class AuthorOutDetail(BaseModel):
    id: int
    name: str
    description: str
    email: EmailStr

    class Config:
        orm_mode = True


class BookOutDetail(BaseModel):
    isbn: str
    title: str
    resume: str
    summary: str
    price: float
    number_of_pages: int
    publish_date: date
    category: CategoryOut
    author: AuthorOutDetail

    class Config:
        orm_mode = True
