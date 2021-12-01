from datetime import date, datetime

from sqlalchemy.orm.session import Session
from casadocodigo.author.model import Author, Book
from casadocodigo.domain.models import Category

def test_can_save_a_author_and_a_book(override_get_db):
    session: Session = override_get_db()
    category = Category(name="Programming")
    book1 = Book(title='Python Rocks!',
                 resume='Python Rocks!',
                 summary='Python Rocks!',
                 price=20.00,
                 publish_date=date.today(),
                 number_of_pages=100,
                 isbn='123456789abcd',
                 category=category)
    book2 = Book(title='Clojure Rocks!',
                 resume='Clojure Rocks!',
                 summary='Clojure Rocks!',
                 price=40.00,
                 publish_date=date.today(),
                 number_of_pages=100,
                 isbn='12c456789abcf',
                 category=category)

    author = Author(name='Fulano', email="fulano@example.com",
                    description="Fulano's description", books=[book1, book2])
    session.add(author)
    session.commit()

    author_db = session.query(Author).first()

    assert author_db.name == 'Fulano'

    assert author_db.books == [book1, book2]
    assert author_db.books[0].category == category
    assert author_db.books[1].category == category
