from datetime import date

from sqlalchemy.orm.session import Session
from casadocodigo.domain.models import Category, Author, Book


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


def test_should_be_able_to_get_a_author_by_book(override_get_db):
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

    author = Author(name='Fulano', email="fulano@fulano.com""",
                    description="Fulano's description", books=[book1, book2])
    session.add(author)
    session.commit()

    book_db = session.query(Book).first()

    assert book_db.author == author
