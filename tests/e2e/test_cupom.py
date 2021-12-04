
from tests.date_utils import make_expire_date
from tests.e2e.api_test import post_cupom


def test_should_create_a_cupom_with_a_valid_code(client):
    _, status_code = post_cupom(client)
    assert status_code == 201


def test_expire_date_should_be_in_the_future(client):
    data, status_code = post_cupom(client, expires_at=make_expire_date(-1))
    assert data == {
        'errors': [{'message': 'expires_at date must be in the future', 'field': 'expires_at'}]
    }


def test_code_should_be_unique(client):
    _, status_code = post_cupom(client)
    assert status_code == 201

    _, status_code = post_cupom(client)
    assert status_code == 400


def test_all_fields_should_be_required(client):
    data, _ = post_cupom(client, code=None, percent_off=None, expires_at=None)
    assert len(data['errors']) == 3
