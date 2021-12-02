from starlette.testclient import TestClient
from api_test import post_category


def test_should_return_400_when_given_a_duplicated_name(client: TestClient):

    category = {"name": "category a"}
    post_category(client, **category)
    data, status_code = post_category(client, **category)
    assert status_code == 400, data
    assert data == {
        'errors': [{'message': 'name already exists', 'field': 'name'}]
    }


def test_should_return_201_when_given_a_valid_category(client: TestClient):
    category = {"name": "category a"}
    data, status_code = post_category(client, **category)
    assert status_code == 201
    assert data['name'] == 'category a'
    assert data['id'] is not None


def test_should_return_422_when_given_a_invalid_category(client: TestClient):
    data, status_code = post_category(client, name=None)
    assert status_code == 422, data
    assert data == {
        'errors': [{'message': 'field required', 'field': 'name'}]
    }
