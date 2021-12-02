from datetime import date
from casadocodigo.domain.models import Author, Book, Category
from pydantic import BaseModel, validator, EmailStr, Field


class AuthorCreate(BaseModel):
    name: str
    description: str = Field(..., max_length=400)
    email: EmailStr

    def to_model(self):
        return Author(name=self.name, description=self.description, email=self.email)


class BookCreate(BaseModel):
    title: str
    resume: str
    summary: str = Field(..., max_length=500)
    price: float = Field(..., ge=20)
    number_of_pages: int = Field(..., ge=100)
    isbn: str
    publish_date: date
    category_id: int

    @validator('publish_date')
    def validate_publish_date(cls, v):
        if date.today() >= v:
            raise ValueError('publish date must be in the future')
        return v

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


class CategoryCreate(BaseModel):
    name: str

    def to_model(self):
        return Category(self.name)
