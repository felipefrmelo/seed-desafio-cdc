from datetime import date, timedelta

from tests.date_utils import make_publish_date


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
