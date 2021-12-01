from datetime import date
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from casadocodigo.domain.models import Author, Book, Category


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


class CategoryCreate(BaseModel):
    name: str

    def to_model(self):
        return Category(self.name)
