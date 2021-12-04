from datetime import date, datetime
from typing import Callable, List, Optional
from casadocodigo.domain.models import Author, Book, Category, Country, Cupom, OrderItem, Payment, State
from pydantic import BaseModel, validator, EmailStr, Field


class AuthorCreate(BaseModel):
    name: str
    description: str = Field(..., max_length=400)
    email: EmailStr

    def to_model(self):
        return Author(name=self.name, description=self.description, email=self.email)

    class Config:
        schema_extra = {
            "example": {
                "name": "J.K. Rowling",
                "description": "J.K. Rowling is a British novelist, screenwriter, and philanthropist. She is best known for her "
                               "novel Harry Potter and her subsequent media franchises, which collectively have grossed over ₹1 "
                               "crore (£1.2 million) for books, ₹500 million for films, and ₹40 billion for television shows.",
                "email": "example@example.com"}
        }


class BookCreate(BaseModel):
    title: str
    resume: str
    summary: str = Field(..., max_length=500)
    price: float = Field(..., ge=20)
    number_of_pages: int = Field(..., ge=100)
    isbn: str
    publish_date: date
    category_id: int

    @ validator('publish_date')
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

    class Config:
        schema_extra = {
            "example": {
                "title": "Harry Potter and the Philosopher's Stone",
                "resume": "Harry Potter and the Philosopher's Stone is a fantasy novel written by British author J. K. Rowling "
                          "and the second novel in the Harry Potter series. It follows Harry Potter, a young wizard, and his "
                          "troubled past, as he learns to discover and harness his unique magical abilities. The plot follows "
                          "Harry's struggle with a series of challenging situations, including the return of the antagonist, "
                          "Dementor, who is a Death Eaters' victim.",
                "summary": "Harry Potter and the Philosopher's Stone is a fantasy novel written by British author J. K. Rowling "
                           "and the second novel in the Harry Potter series. It follows Harry Potter, a young wizard, and his "
                           "troubled past, as he learns to discover and harness his unique magical abilities. The plot follows "
                           "Harry's struggle with a series of challenging situations, including the return of the antagonist, "
                           "Dementor, who is a Death Eaters' victim.",
                "price": 20.0,
                "number_of_pages": 300,
                "isbn": "9780747532743",
                "publish_date": "2000-01-01",
                "category_id": 1}
        }


class CategoryCreate(BaseModel):
    name: str

    def to_model(self):
        return Category(self.name)

    class Config:
        schema_extra = {
            "example": {
                "name": "Fiction"}
        }


class CountryCreate(BaseModel):
    name: str

    def to_model(self):
        return Country(self.name)

    class Config:
        schema_extra = {
            "example": {
                "name": "Brazil"}
        }


class StateCreate(BaseModel):
    name: str

    def to_model(self):
        return State(self.name)

    class Config:
        schema_extra = {
            "example": {
                "name": "RJ"}
        }


class ItemCart(BaseModel):
    title: str
    quantity: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "title": "Harry Potter and the Philosopher's Stone",
                "quantity": 1}
        }


class Cart(BaseModel):
    total: float = Field(..., gt=0)
    items: List[ItemCart] = Field(..., min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "total": 20.0,
                "items": [
                    {
                        "title": "Harry Potter and the Philosopher's Stone",
                        "quantity": 1
                    }
                ]}
        }


class PaymentCreate(BaseModel):
    name: str
    email: EmailStr
    last_name: str
    document: str
    adrress: str
    complement: str
    country_id: str
    city: str
    state_name: Optional[str]
    phone: str
    zip_code: str
    cart: Cart
    cupom_code: Optional[str]

    @ validator('document')
    def validate_document(cls, v):
        if 14 != len(v) != 11:
            raise ValueError('document must be a valid cpf or 14 cnpj')
        return v

    def to_model(self, country: Country, cart: List[OrderItem], valid_cupom: Callable[[str], Cupom]):
        state = country.get_state(self.state_name)
        cupom = valid_cupom(self.cupom_code) if self.cupom_code else None
        return Payment(
            name=self.name,
            email=self.email,
            last_name=self.last_name,
            document=self.document,
            adrress=self.adrress,
            complement=self.complement,
            country=country,
            city=self.city,
            state=state,
            phone=self.phone,
            zip_code=self.zip_code,
            cart=cart,
            cupom=cupom
        )

    class Config:
        schema_extra = {
            "example": {
                "name": "J.K. Rowling",
                "email": "example@example.com",
                "last_name": "J.K. Rowling",
                "document": "12345678901",
                "adrress": "Rua do exemplo",
                "complement": "Apto 101",
                "country_id": "1",
                "city": "São Paulo",
                "state_name": "SP",
                "phone": "11 99999-9999",
                "zip_code": "01001000",
                "cart": {
                    "total": 20.0,
                    "items": [
                        {
                            "title": "Harry Potter and the Philosopher's Stone",
                            "quantity": 1
                        }
                    ]
                },
                "cupom_code": "123456789"}
        }


class CupomCreate(BaseModel):
    code: str
    percent_off: float
    expires_at: datetime

    def to_model(self):
        return Cupom(
            code=self.code,
            percent_off=self.percent_off,
            expires_at=self.expires_at
        )

    @ validator('expires_at')
    def validate_publish_date(cls, v):
        if datetime.utcnow() >= v:
            raise ValueError('expires_at date must be in the future')
        return v

    class Config:
        schema_extra = {
            "example": {
                "code": "123456789",
                "percent_off": 10.0,
                "expires_at": "2020-01-01"}
        }
