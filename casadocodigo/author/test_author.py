from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from requests.models import Response


def post_author(client, **data):
    data = {"name": 'test', 'email': 'test@test.comm',
            'description': "descrição do autor", **data}
    response = client.post("/author/", json=data)
    return response.json(), response.status_code


class TestAuthor:

    def test_create_author(self, client: TestClient):

        data, status_code = post_author(client)
        assert status_code == 201
        assert data['id'] is not None
        assert data['created_at'] is not None

    def test_should_return_422_when_given_a_invalid_email(self, client: TestClient):

        data, status_code = post_author(client, email='invalid-email')
        assert status_code == 422
        assert data == {
            'errors': [{'message': 'value is not a valid email address', 'field': 'email'}]
        }

    def test_should_return_a_body_with_errors(self, client: TestClient):
        response = client.post("/author/", json={})

        errors = response.json()["errors"]
        assert response.status_code == 422
        assert len(errors) == 3
        for error in errors:
            assert error['message'] == 'field required'

    def test_the_description_cannot_exceed_400_characters(self, client: TestClient):

        data, _ = post_author(client, description="des "*100 + "a")
        assert data["errors"][0] == {
            "field": 'description', 'message': "ensure this value has at most 400 characters"}

    def test_should_return_400_when_given_a_duplicated_email(self, client: TestClient):

        post_author(client)
        data, status_code = post_author(client)
        assert status_code == 400
        assert data == {
            'errors': [{'message': 'email already exists', 'field': 'email'}]
        }
