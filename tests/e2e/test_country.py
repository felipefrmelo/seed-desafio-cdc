
from tests.e2e.api_test import post_country, post_state


def test_should_create_country(client):
    response = post_country(client)

    assert response.status_code == 201
    assert response.json()['name'] == 'Brazil'


def test_cannot_create_country_with_same_name(client):
    post_country(client)

    response = post_country(client)

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'name already exists', 'field': 'name'}]
    }


def test_shoud_create_state(client):
    response = post_country(client)

    assert response.status_code == 201

    country_id = response.json()["id"]
    response = post_state(client, country_id)

    assert response.status_code == 201
    assert response.json()['name'] == 'Rio de Janeiro'


def test_cannot_create_state_with_same_name(client):
    response = post_country(client)
    country_id = response.json()["id"]

    assert response.status_code == 201

    response = post_state(client, country_id)

    assert response.status_code == 201

    response = post_state(client, country_id)

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'name already exists', 'field': 'name'}]
    }
