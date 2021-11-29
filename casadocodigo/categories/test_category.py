from starlette.testclient import TestClient


def test_should_return_400_when_given_a_duplicated_name(client: TestClient):

    category = {"name": "category a"}
    client.post('/category/', json=category)
    response = client.post('/category/', json=category)
    assert response.status_code == 400, response.json()
    assert response.json() == {
        'errors': [{'message': 'category already exists', 'field': 'category'}]
    }


def test_should_return_201_when_given_a_valid_category(client: TestClient):
    category = {"name": "category a"}
    response = client.post('/category/', json=category)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'category a'
    assert data['id'] is not None


def test_should_return_422_when_given_a_invalid_category(client: TestClient):
    category = {}
    response = client.post('/category/', json=category)
    assert response.status_code == 422, response.json()
    assert response.json() == {
        'errors': [{'message': 'field required', 'field': 'name'}]
    }
