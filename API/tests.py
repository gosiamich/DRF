import pytest
import pytz
from faker import Faker
from django.conf.global_settings import TIME_ZONE

from rest_api_app.models import Author, Book

faker = Faker("pl_PL")
TZ = pytz.timezone(TIME_ZONE)


@pytest.mark.django_db
def test_get_book_list(client, book):
    response = client.get("/generic_list_book/", {}, format='json')
    assert response.status_code == 200
    assert Book.objects.count() == len(response.data)


@pytest.mark.django_db
def test_book_add(client):
    new_book = {
        'title': 'New title'
    }
    response = client.post("/generic_list_book/", new_book, format='json')
    assert response.status_code == 201
    for key, value in new_book.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_get_book_detail(client, book):
    response = client.get(f"/generic_detail_book/{book.id}/", {}, format='json')
    assert response.status_code == 200
    for field in ("title",):
        assert field in response.data



@pytest.mark.django_db
def test_AuthorViewSet_list(client, author):
    response = client.get(f"/authors/", {}, format='json')
    assert response.status_code == 200
    assert Author.objects.count() == len(response.data)


@pytest.mark.django_db
def test_AuthorViewSet_detail(client, author):
    response = client.get(f"/authors/{author.id}/", {}, format='json')
    assert response.status_code == 200
    for field in ("name",):
        assert field in response.data


@pytest.mark.django_db
def test_AuthorViewSet_delete(client, author):
    response = client.delete(f"/authors/{author.id}/", {}, format='json')
    assert response.status_code == 204
    authors_ids = [author.id for author in Author.objects.all()]
    assert author.id not in authors_ids
    with pytest.raises(author.DoesNotExist):
        Author.objects.get(id=author.id)


@pytest.mark.django_db
def test_AuthorViewSet_add(client):
    new_author = {
        'name': 'New author'
    }
    response = client.post("/authors/", new_author, format='json')
    assert response.status_code == 201
    for key, value in new_author.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_AuthorViewSet_update(client, author):
    response = client.get(f"/authors/{author.id}/", {}, format='json')
    input_data = response.data
    input_data["name"] = 'New name'
    response = client.patch(f"/authors/{author.id}/", input_data, format='json')
    assert response.status_code == 200
    author.refresh_from_db()
    assert author.name == 'New name'

""""
"""

@pytest.mark.django_db
def test_BookViewSet_list(client, book):
    response = client.get(f"/books_api/", {}, format='json')
    assert response.status_code == 200
    assert Book.objects.count() == len(response.data)


@pytest.mark.django_db
def test_BookViewSet_detail(client, book):
    response = client.get(f"/books_api/{book.id}/", {}, format='json')
    assert response.status_code == 200
    for field in ("title",):
        assert field in response.data


@pytest.mark.django_db
def test_BookViewSet_delete(client, book):
    response = client.delete(f"/books_api/{book.id}/", {}, format='json')
    assert response.status_code == 204
    books_id = [book.id for book in Book.objects.all()]
    assert book.id not in books_id
    with pytest.raises(book.DoesNotExist):
        Book.objects.get(id=book.id)


@pytest.mark.django_db
def test_BookViewSet_add(client):
    new_book = {
        'title': 'New title'
    }
    response = client.post("/books_api/", new_book, format='json')
    assert response.status_code == 201
    for key, value in new_book.items():
        assert key in response.data
        assert response.data[key] == value


@pytest.mark.django_db
def test_BookViewSet_update(client, book):
    response = client.get(f"/books_api/{book.id}/", {}, format='json')
    input_data = response.data
    input_data["title"] = 'New title'
    response = client.patch(f"/books_api/{book.id}/", input_data, format='json')
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == 'New title'


