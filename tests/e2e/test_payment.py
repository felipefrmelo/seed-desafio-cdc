from datetime import datetime, timedelta
from tests.e2e.api_test import create_books, post_country, post_cupom, post_pay, post_state
import pytest
from time import sleep


@pytest.fixture
def cart(client, author_id, category_id):
    result = create_books(client, author_id, category_id, 5)

    return lambda total= None: {
        "total": total if total else sum(book['price'] for book in result),
        "items": [{"title": b['title'], "quantity": 1} for b in result]
    }


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


def test_should_create_a_payment(client, country_id, state_name, cart):
    response = post_pay(client, country_id, state_name, cart())

    assert response.status_code == 201

def test_state_can_be_null(client,  cart):
    response = post_country(client)
   
    response = post_pay(client, response.json()["id"], None, cart())

    assert response.status_code == 201


def test_document_should_be_cpf_or_cnpj(client, country_id, state_name, cart):
    response = post_pay(client, country_id, state_name, cart(),
                        document='19218218921828193819831981')

    assert response.status_code == 422
    assert response.json() == {
        'errors': [{'message': 'document must be a valid cpf or 14 cnpj', 'field': 'document'}]

    }


def test_state_should_be_belong_to_country(client, country_id, cart):

    response = post_pay(client, country_id, 1212121, cart())

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'state must be belong to country'}]

    }


def test_should_return_404_when_country_not_found(client, cart):
    response = post_pay(client, 1212121, 'Test', cart())

    assert response.status_code == 404
    assert response.json() == {
        'errors': [{'message': 'country not found'}]

    }


def test_should_return_400_when_cart_total_not_equal_to_payment_total(client, country_id, state_name, cart):
    response = post_pay(client, country_id, state_name, cart(total=895746321))

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'cart total is invalid'}]

    }


def test_code_of_cupom_should_be_valid(client, country_id, state_name, cart):
    response = post_pay(client, country_id, state_name,
                        cart(), cupom_code='123456789')

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'cupom invalid (123456789)'}]

    }


def test_cupom_is_invalid_when_expires(client, country_id, state_name, cart):
    expires_at = datetime.utcnow() + timedelta(milliseconds=100)

    _, status_code = post_cupom(
        client, code='cupom123', expires_at=expires_at.isoformat())
    assert status_code == 201
    sleep(0.1)

    response = post_pay(client, country_id, state_name,
                        cart(), cupom_code='cupom123')

    assert response.status_code == 400
    assert response.json() == {
        'errors': [{'message': 'cupom invalid (cupom123)'}]

    }


def test_get_detail_of_payment(client, country_id, state_name, cart):
    post_cupom(client, code='cupom123', percent_off=10)

    cart = cart()
    response = post_pay(client, country_id, state_name,
                        cart, cupom_code='cupom123')

    assert response.status_code == 201

    response = client.get(f'/payment/{response.json()["id"]}')

    assert response.status_code == 200
    data = response.json()
    assert data['total'] == cart['total']
    assert len(data['items']) == len(cart['items'])
    assert data['total_with_discount'] == cart['total'] - (cart['total'] * 0.1)
    assert data['discount'] == cart['total'] * 0.1
    assert data['cupom'] == {'code': 'cupom123',
                             'percent_off': 10}
