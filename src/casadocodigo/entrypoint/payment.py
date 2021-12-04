from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from casadocodigo.domain.models import Country, Book, Cupom, OrderItem, Payment

from casadocodigo.service_layer.In import ItemCart, PaymentCreate
from casadocodigo.service_layer.Out import PaymentOut, PaymentOutDetail
from casadocodigo.service_layer.errors import CountryNotFound, ValidationException

from ..dependencies import get_db


app = APIRouter(prefix="/payment", tags=["payment"])


def make_cart(db: Session, items: List[ItemCart]):
    books = db.query(Book).filter(
        Book.title.in_(item.title for item in items)).all()  # type: ignore
    if len(books) != len(items):
        book_not_found = set(item.title for item in items) - set(
            book.title for book in books)
        raise ValidationException(f"Book not found ({book_not_found})")
    return [OrderItem(item.title, item.quantity, book.price) for book, item in zip(books, items)]


def valid_cupom(db: Session):
    def wrapper(cupom_code: str) -> Cupom:
        cupom = db.query(Cupom).filter_by(code=cupom_code).first()
        if cupom is None or cupom.is_valid() is False:
            raise ValidationException(f"cupom invalid ({cupom_code})")
        return cupom
    return wrapper


@app.post("/", response_model=PaymentOut,  status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    country: Country = db.query(Country).filter_by(
        id=payment.country_id).first()

    if not country:
        raise CountryNotFound()

    if payment.state_name:
        state = country.get_state(payment.state_name)
        if not state:
            raise ValidationException("state must be belong to country")

    cart = make_cart(db, payment.cart.items)

    pay = payment.to_model(country, cart, valid_cupom(db))

    if pay.total != payment.cart.total:
        raise ValidationException("cart total is invalid")

    db.add(pay)
    db.commit()

    paymentOut = PaymentOut(
        id=pay.id,
        total=pay.total,
        email=pay.email,
        name=pay.name)
    return paymentOut


@app.get("/{payment_id}", response_model=PaymentOutDetail)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter_by(id=payment_id).first()
    if not payment:
        raise ValidationException("payment not found")
    paymentDetail = PaymentOutDetail(id=payment.id,
                                     total=payment.total,
                                     items=payment.cart,
                                     total_with_discount=payment.total_with_discount,
                                     discount=payment.discount,
                                     cupom=payment.cupom)
    return paymentDetail
