from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import pytest

from .main import app, get_db
from .orm import metadata

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
    engine.execute("DELETE FROM author")


def makeUserData(**kwargs):
    return {"name": 'felipe', 'email': 'felipe@gmail.comm', 'description': "descrição do autor", **kwargs}


def test_create_author(cleanup):

    user = makeUserData()
    response = client.post(
        "/author/",
        json=user)

    assert response.status_code == 201, response.json()
    data = response.json()
    createdAt = datetime.fromisoformat(data.pop("createdAt"))
    Id = data.pop("id")
    assert data == user
    assert Id is not None
    assert datetime.utcnow() - \
        createdAt < timedelta(seconds=1)


def test_should_return_422_when_given_a_invalid_email():

    response = client.post(
        "/author/",
        json=makeUserData(email='invalid-email'))
    assert response.status_code == 422
    assert response.json() == {
        'errors': [{'message': 'value is not a valid email address', 'field': 'email'}]
    }


def test_should_return_a_body_with_errors():

    response = client.post(
        "/author/",
        json={})

    assert response.status_code == 422
    errors = response.json()["errors"]
    assert len(errors) == 3
    for error in errors:
        assert error["message"] == 'field required'


def test_the_description_cannot_exceed_400_characters():

    responses = client.post('/author/',
                            json=makeUserData(description="des "*100 + "a"))

    assert responses.json()["errors"][0] == {
        "field": 'description', 'message': "ensure this value has at most 400 characters"}


def test_should_return_400_when_given_a_duplicated_email(cleanup):

    user = makeUserData()
    client.post('/author/', json=user)
    response = client.post('/author/', json=user)
    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'email already exists', 'field': 'email'}]
    }
