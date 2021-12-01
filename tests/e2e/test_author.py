from datetime import date
from fastapi.testclient import TestClient
import pytest


def post_author(client, **data):
    data = {"name": 'test', 'email': 'test@test.comm',
            'description': "descrição do autor", **data}
    response = client.post("/author/", json=data)
    return response.json(), response.status_code


def post_category(client, **data):
    data = {"name": 'programming', **data}
    response = client.post("/category/", json=data)
    return response.json(), response.status_code


def post_book(client, author_id, category_id, **data):
    data = {"title": 'test', 'resume': 'test',
            'summary': "descrição do livro", 'price': 100.0,
            'number_of_pages': 100, 'isbn': '123456789',
            'publish_date': date.today().__str__(), 'category_id': category_id, **data}

    response = client.post(f"/author/{author_id}/book", json=data)
    return response.json(), response.status_code


@pytest.fixture
def author_id(client):
    data = post_author(client)
    return data[0]['id']


@pytest.fixture
def category_id(client):
    data = post_category(client)
    return data[0]['id']


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


class TestBook:

    def test_should_create_a_book(self, client: TestClient, author_id, category_id):

        data, status_code = post_book(client, author_id, category_id)

        assert status_code == 201

    @pytest.mark.parametrize("field, value", [
        ('title', None),
        ('resume', None),
        ('summary', None),
        ('price', None),
        ('number_of_pages', None),
        ('isbn', None),
        ('publish_date', None),
        ('category_id', None),
    ])
    def test_should_return_400_when_given_a_invalid_field(self, client: TestClient, author_id, category_id, field, value):
        data, status_code = post_book(
            client, author_id,  **{"category_id": category_id, field: value})

        assert status_code == 422
        assert data == {
            'errors': [{'message': 'none is not an allowed value', 'field': field}]
        }

    def test_price_should_not_be_smaller_than_20(self, client: TestClient, author_id, category_id):
        data, status_code = post_book(
            client, author_id, category_id, price=19.99)

        assert status_code == 422
        assert data == {
            'errors': [{'message': 'ensure this value is greater than or equal to 20', 'field': 'price'}]
        }

    def test_should_summary_is_not_greater_than_500_characters(self, client: TestClient, author_id, category_id):
        data, status_code = post_book(
            client, author_id, category_id, summary="s"*501)

        assert status_code == 422
        assert data == {
            'errors': [{'message': 'ensure this value has at most 500 characters', 'field': 'summary'}]
        }

    def test_should_return_400_when_given_a_duplicated_isbn(self, client: TestClient, author_id, category_id):
        post_book(client, author_id, category_id)
        data, status_code = post_book(client, author_id, category_id)

        assert status_code == 400
        assert data == {
            'errors': [{'message': 'isbn already exists', 'field': 'isbn'}]
        }
