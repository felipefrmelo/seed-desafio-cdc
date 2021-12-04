from datetime import date, timedelta

from tests.date_utils import make_expire_date, make_publish_date


def remove_key_with_none_value(dictionary):
    return {k: v for k, v in dictionary.items() if v is not None}


def post_author(client, **data):

    clean_data = remove_key_with_none_value({"name": 'test', 'email': 'test@test.comm',
                                             'description': "descrição do autor", **data})
    response = client.post("/author/", json=clean_data)
    return response.json(), response.status_code


def post_category(client, **data):

    clean_data = remove_key_with_none_value({"name": 'programming', **data})
    response = client.post("/category/", json=clean_data)
    return response.json(), response.status_code


def post_book(client, author_id, category_id, **data):
    clean_data = remove_key_with_none_value({"title": 'test', 'resume': 'test',
                                             'summary': "descrição do livro", 'price': 100.0,
                                             'number_of_pages': 100, 'isbn': '123456789',
                                             'publish_date':  make_publish_date(),
                                             'category_id': category_id, **data})

    response = client.post(f"/author/{author_id}/book", json=clean_data)
    return response.json(), response.status_code


def post_state(client, country_id):
    response = client.post(f'country/{country_id}/state', json={
        'name': 'Rio de Janeiro',
    })
    return response


def post_country(client):
    return client.post('/country/', json={'name': 'Brazil', })


def create_books(client, author_id, category_id, number_of_books):
    books = []
    for i in range(number_of_books):
        data, _ = post_book(
            client, author_id,  **{"category_id": category_id, "title": f"Book {i}", 'isbn': f"isbn {i}"})
        books.append(data)
    return books


def post_cupom(client, **kwargs):
    response = client.post('/cupoms/', json={
        'code': '1234567890',
        'percent_off': 10,
        'expires_at': make_expire_date(),
        ** kwargs
    })

    return response.json(), response.status_code


def post_pay(client,  customer_id, cart, **kwargs):
    response = client.post('/payment/', json={
        'customer_id':customer_id,
        'cart': cart,
        **kwargs
    })
    return response

def post_customer(client, country_id, state_name, **kwargs):
    response = client.post('/customer/', json={
        'name': 'Test',
        'email': 'test@test.com',
        'last_name': 'Test',
        "document": "12345678912",
        'adrress': 'Rua Teste',
        'complement': 'Teste',
        'country_id': country_id,
        'city': 'Test',
        'state_name': state_name,
        'phone': '123456789',
        'zip_code': '12345678',
        **kwargs
    })


    return response.json(), response.status_code
