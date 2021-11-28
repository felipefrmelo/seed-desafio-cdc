from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import pytest

from ..main import app
from ..dependencies import get_db
from ..orm import metadata

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

metadata.create_all(bind=engine)


def override_get_db():
    try:
        db: Session = TestingSessionLocal()
        yield db
    finally:
        db.close()  # type: ignore


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def cleanup():
    yield
    engine.execute("DELETE FROM category")


def test_should_return_400_when_given_a_duplicated_name(cleanup):

    category = {"name": "category a"}
    client.post('/category/', json=category)
    response = client.post('/category/', json=category)
    assert response.status_code == 400, response.json()
    assert response.json() == {
        'errors': [{'message': 'category already exists', 'field': 'category'}]
    }


def test_should_return_201_when_given_a_valid_category(cleanup):
    category = {"name": "category a"}
    response = client.post('/category/', json=category)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'category a'
    assert data['id'] is not None


def test_should_return_422_when_given_a_invalid_category(cleanup):
    category = {}
    response = client.post('/category/', json=category)
    assert response.status_code == 422, response.json()
    assert response.json() == {
        'errors': [{'message': 'field required', 'field': 'name'}]
    }
