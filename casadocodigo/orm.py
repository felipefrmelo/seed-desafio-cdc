from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import registry
from .author.model import Author
from .categories.model import Category

mapper_registry = registry()
metadata = MetaData()

author = Table(
    'author',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('description', String(400)),
    Column('email', String(50), unique=True,  index=True),
)

category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True,  index=True, ),

)


mapper_registry.map_imperatively(Author, author)

mapper_registry.map_imperatively(Category, category)
