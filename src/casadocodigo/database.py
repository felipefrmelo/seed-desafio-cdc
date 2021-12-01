from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlapp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
