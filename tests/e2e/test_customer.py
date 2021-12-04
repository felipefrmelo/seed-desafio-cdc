from datetime import datetime, timedelta
from tests.e2e.api_test import post_country, post_customer,  post_state
import pytest


@pytest.fixture
def country_id(client):
    response = post_country(client)
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture
def state_name(client, country_id):
    response = post_state(client, country_id)
    assert response.status_code == 201
    return response.json()["name"]




def test_document_should_be_cpf_or_cnpj(client, country_id, state_name):
    data, status_code = post_customer(client, country_id, state_name,
                             document='19218218921828193819831981')

    assert status_code == 422
    assert data == {
        'errors': [{'message': 'document must be a valid cpf or 14 cnpj', 'field': 'document'}]

    }


def test_state_should_be_bdataelong_to_country(client, country_id):

    data, status_code = post_customer(client, country_id, 'Test')

    assert status_code == 400
    assert data == {
        'errors': [{'message': 'state must be belong to country'}]

    }


def test_should_return_404_when_country_not_found(client):
    data, status_code = post_customer(client, 1212121, 'Test')

    assert status_code == 404
    assert data == {
        'errors': [{'message': 'country not found'}]

    }

def test_customer_email_should_be_unique(client, country_id, state_name):
    post_customer(client, country_id, state_name)
    data, status_code = post_customer(client, country_id, state_name)

    assert status_code == 400
    assert data == {
        'errors': [{'message': "email already exists", 'field': "email"}]
    }







