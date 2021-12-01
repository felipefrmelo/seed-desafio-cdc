from dataclasses import dataclass, field
from typing import List
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
