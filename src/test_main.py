from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from .main import app


client = TestClient(app)


def makeUserData(**kwargs):
    return {"name": 'felipe', 'email': 'felipe@gmail.com', 'description': "descrição do autor", **kwargs}


def test_create_author():

    response = client.post(
        "/author/",
        json=makeUserData())

    assert response.status_code == 201
    data = response.json()
    createdAt = datetime.fromisoformat(data.pop("createdAt"))
    assert data == makeUserData()
    assert datetime.now(timezone.utc) - \
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
