from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime, date


@dataclass
class Category:
    id: int = field(init=False)
    name: str


@dataclass
class Book:
    title: str
    resume: str
    summary: str
    price: float
    number_of_pages: int
    isbn: str
    publish_date: date
    category: Category


@dataclass
class Author:
    id: int = field(init=False)
    name: str
    email: str
    description: str
    books: List[Book] = field(default_factory=list)
    created_at: datetime = field(init=False)

    def add_book(self, book: Book):
        self.books.append(book)


@dataclass(unsafe_hash=True)
class State:
    id: int = field(init=False)
    name: str


@dataclass
class Country:
    id: int = field(init=False)
    name: str
    states: Set[State] = field(default_factory=set)

    def create_state(self, state: State):
        self.states.add(state)

    def get_state(self, state_name: str):
        for state in self.states:
            if state.name == state_name:
                return state
        return None


@dataclass
class OrderItem:
    id: int = field(init=False)
    title: str
    quantity: int
    price: float


@dataclass
class Cupom:
    id: int = field(init=False)
    code: str
    percent_off: float
    expires_at: datetime

    def is_valid(self):
        return self.expires_at > datetime.utcnow()


@dataclass
class Payment:
    id: int = field(init=False)
    name: str
    email: str
    last_name: str
    document: str
    adrress: str
    complement: str
    country: Country
    city: str
    phone: str
    zip_code: str
    cart: List[OrderItem] = field(default_factory=list)
    state: Optional[State] = field(default=None)
    cupom: Optional[Cupom] = field(default=None)

    @property
    def total(self):
        return sum([item.price * item.quantity for item in self.cart])

    @property
    def total_with_discount(self):
        if self.cupom is None:
            return self.total
        return self.total * (1 - self.cupom.percent_off / 100)

    @property
    def discount(self):
        if self.cupom is None:
            return 0
        return self.total - self.total_with_discount
