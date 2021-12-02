from datetime import date
from fastapi.testclient import TestClient
from api_test import post_author, post_category, post_book
import pytest
from random import randint


@pytest.fixture
def author_id(client):
    data = post_author(client)
    return data[0]['id']


@pytest.fixture
def category_id(client):
    data = post_category(client)
    return data[0]['id']


def create_books(client: TestClient, author_id, category_id, number_of_books):
    books = []
    for i in range(number_of_books):
        data, _ = post_book(
            client, author_id,  **{"category_id": category_id, "title": f"Book {i}", 'isbn': f"isbn {i}"})
        books.append(data)
    return books


def test_get_books(client: TestClient, author_id, category_id):
    number_of_books = randint(1, 10)
    books = create_books(client, author_id, category_id, number_of_books)
    response = client.get('/books/')
    assert response.status_code == 200
    assert len(response.json()) == number_of_books
    for book in response.json():
        assert book['title']
        assert book['isbn']


def test_get_book_by_title(client: TestClient, author_id, category_id):
    number_of_books = 1
    book, = create_books(client, author_id, category_id, number_of_books)
    response = client.get(f'/books/{book["title"]}')
    data, status_code = response.json(), response.status_code
    assert status_code == 200
    assert data['title'] == book['title']
    assert data['isbn'] == book['isbn']
    assert data['category']['id'] == category_id
    assert data['category']['name']
    assert data['resume']
    assert data['summary']
    assert data['price']
    assert data['number_of_pages']
    assert data['publish_date']
    assert data['author']['id'] == author_id
    assert data['author']['name']
    assert data['author']['email']
    assert data['author']['description']


def test_should_return_404_when_book_not_found(client: TestClient, author_id, category_id):
    number_of_books = 1
    book, = create_books(client, author_id, category_id, number_of_books)
    response = client.get(f'/books/{book["title"]}-not-found')
    assert response.status_code == 404
    assert response.json()['errors'] == [{'message': 'book not found'}]
