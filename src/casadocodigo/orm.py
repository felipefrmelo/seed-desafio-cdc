from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import backref, registry, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from .domain.models import Author, Book, Category, Country, Cupom, Customer, OrderItem, Payment, State

mapper_registry = registry()
metadata = MetaData()

author = Table(
    'author',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('description', String(400)),
    Column('email', String(50), unique=True,  index=True),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow)
)


category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True,  index=True, ),

)

book = Table(
    'book',
    metadata,
    Column('isbn', String(13), nullable=False,  primary_key=True),
    Column('title', String(100), nullable=False),
    Column('resume', String(500), nullable=False),
    Column('summary', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('number_of_pages', Integer, nullable=False),
    Column('publish_date', Date, nullable=False),
    Column('author_id', Integer, ForeignKey('author.id'), nullable=False),
    Column('category_id', Integer, ForeignKey('category.id'), nullable=False),

)

country = Table(
    'country',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True,  index=True, ),

)

state = Table(
    'state',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True,  index=True, ),
    Column('country_id', Integer, ForeignKey('country.id'), nullable=False),
)
order_item = Table(
    'order_item',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('price', Float, nullable=False),
    Column('title', Integer, ForeignKey('book.title'), nullable=False),
    Column('payment_id', Integer, ForeignKey('payment.id'), nullable=False),
)

customer = Table(
    'customer',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('email', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('document', String(20), nullable=False),
    Column('adrress', String(200), nullable=False),
    Column('complement', String(200), nullable=False),
    Column('country_id', Integer, ForeignKey('country.id'), nullable=False),
    Column('city', String(50), nullable=False),
    Column('phone', String(50), nullable=False),
    Column('zip_code', String(50), nullable=False),
    Column('state_id', Integer, ForeignKey('state.id')),
)

payment = Table(
    'payment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer, ForeignKey('customer.id')),
    Column('cupom_id', Integer, ForeignKey('cupom.id')),
)

cupom = Table(
    'cupom',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(50), unique=True,  index=True),
    Column('percent_off', Float, nullable=False),
    Column('expires_at', DateTime, nullable=False),
)
mapper_registry.map_imperatively(Cupom, cupom)

mapper_registry.map_imperatively(Author, author, properties={
    'books': relationship(Book, backref='author')
})

mapper_registry.map_imperatively(Category, category)

mapper_registry.map_imperatively(Book, book, properties={
    'category': relationship(Category, backref='books'),
})

mapper_registry.map_imperatively(Country, country, properties={
    'states': relationship(State, collection_class=set, backref="country")
})

mapper_registry.map_imperatively(State, state)

mapper_registry.map_imperatively(OrderItem, order_item, properties={
    'book': relationship(Book, backref='order_item')
})

mapper_registry.map_imperatively(Customer, customer, properties={
    'country': relationship(Country),
    'state': relationship(State),
})


mapper_registry.map_imperatively(Payment, payment, properties={
    'cart': relationship(OrderItem,  backref='payment'),
    'cupom': relationship(Cupom),
    'customer': relationship(Customer)
})
