from datetime import date
from fastapi.testclient import TestClient
from api_test import post_author, post_category, post_book
import pytest

from tests.date_utils import make_publish_date


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

        _, status_code = post_book(client, author_id, category_id)

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
            'errors': [{'message': 'field required', 'field': field}]
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

    def test_number_of_pages_should_be_greater_than_100(self, client: TestClient, author_id, category_id):
        data, status_code = post_book(
            client, author_id, category_id, number_of_pages=99)

        assert status_code == 422
        assert data == {
            'errors': [{'message': 'ensure this value is greater than or equal to 100', 'field': 'number_of_pages'}]
        }

    def test_title_should_not_be_duplicated(self, client: TestClient, author_id, category_id):
        post_book(client, author_id, category_id, title="title")
        data, status_code = post_book(
            client, author_id, category_id, title="title", isbn='1234567890abc')

        assert status_code == 400
        assert data == {
            'errors': [{'message': 'title already exists', 'field': 'title'}]
        }

    def test_publish_date_should_be_in_the_future(self, client: TestClient, author_id, category_id):

        data, status_code = post_book(
            client, author_id, category_id, publish_date=make_publish_date(days_in_future=0))
        assert status_code == 422
        assert data == {
            'errors': [{'message': 'publish date must be in the future', 'field': 'publish_date'}]
        }

    def test_should_return_404_when_given_a_author_id_that_does_not_exist(self, client: TestClient, category_id):
        data, status_code = post_book(client, 9999, category_id)

        assert status_code == 404
        assert data == {
            'errors': [{'message': 'author not found'}]
        }

    def test_should_return_404_when_given_a_category_id_that_does_not_exist(self, client: TestClient, author_id):
        data, status_code = post_book(client, author_id, category_id=9999)

        assert status_code == 404
        assert data == {
            'errors': [{'message': 'category not found'}]
        }

    def test_should_return_400_when_given_a_duplicated_isbn(self, client: TestClient, author_id, category_id):
        post_book(client, author_id, category_id)
        data, status_code = post_book(
            client, author_id, category_id, title='other title')

        assert status_code == 400
        assert data == {
            'errors': [{'message': 'isbn already exists', 'field': 'isbn'}]
        }
