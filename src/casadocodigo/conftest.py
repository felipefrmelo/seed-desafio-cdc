import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from .main import app
from .orm import metadata
from .dependencies import get_db


@pytest.fixture
def sqlite_db():
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(sqlite_db):
    yield sessionmaker(
        autocommit=False, autoflush=False, bind=sqlite_db)


@pytest.fixture
def override_get_db(sqlite_session_factory):
    db: Session = None
    try:
        db = sqlite_session_factory()
        yield lambda: db
    finally:
        db.close()


@pytest.fixture
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
