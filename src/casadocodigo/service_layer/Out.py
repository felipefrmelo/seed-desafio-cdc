from datetime import date, datetime
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


class CountryOut(BaseModel):
    id: int
    name: str


class StateOut(BaseModel):
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


class PaymentOut(BaseModel):
    id: int
    total: float

class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr


class CupomOut(BaseModel):
    code: str
    percent_off: float

    class Config:
        orm_mode = True


class PaymentOutDetail(BaseModel):
    id: int
    total:  float
    items:  list
    total_with_discount: float
    discount: float
    cupom: CupomOut
