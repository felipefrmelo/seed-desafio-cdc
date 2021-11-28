from enum import unique
from operator import index
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from . import model

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


mapper_registry.map_imperatively(model.Author, author)


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlapp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
