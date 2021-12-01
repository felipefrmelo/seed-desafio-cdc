from datetime import datetime
from sqlalchemy import Column, Integer, MetaData, String, Table, Date, Text, DateTime, Float
from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from .author.model import Author, Book
from .domain.models import Category

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

mapper_registry.map_imperatively(Author, author, properties={
    'books': relationship(Book, backref='author')
})

mapper_registry.map_imperatively(Category, category)

mapper_registry.map_imperatively(Book, book, properties={
    'category': relationship(Category, backref='books'),
})
