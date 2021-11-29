from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def makeUserData(**kwargs):
    return {"name": 'felipe', 'email': 'felipe@gmail.comm', 'description': "descrição do autor", **kwargs}


def test_create_author(client: TestClient):

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
        createdAt < timedelta(seconds=0.1)


def test_should_return_422_when_given_a_invalid_email(client: TestClient):

    response = client.post(
        "/author/",
        json=makeUserData(email='invalid-email'))
    assert response.status_code == 422
    assert response.json() == {
        'errors': [{'message': 'value is not a valid email address', 'field': 'email'}]
    }


def test_should_return_a_body_with_errors(client: TestClient):

    response = client.post(
        "/author/",
        json={})

    assert response.status_code == 422
    errors = response.json()["errors"]
    assert len(errors) == 3
    for error in errors:
        assert error["message"] == 'field required'


def test_the_description_cannot_exceed_400_characters(client: TestClient):

    responses = client.post('/author/',
                            json=makeUserData(description="des "*100 + "a"))

    assert responses.json()["errors"][0] == {
        "field": 'description', 'message': "ensure this value has at most 400 characters"}


def test_should_return_400_when_given_a_duplicated_email(client: TestClient):

    user = makeUserData()
    client.post('/author/', json=user)
    response = client.post('/author/', json=user)
    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'email already exists', 'field': 'email'}]
    }
