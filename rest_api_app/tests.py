from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
import pytest
from django.urls import reverse

from rest_api_app.forms import SearchForm
from rest_api_app.models import Book, Author


@pytest.mark.django_db
def test_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_my_user(user):
    assert user.is_superuser


@pytest.mark.django_db
def test_filter_book(book):
    assert Book.objects.filter(title="Books").exists()


@pytest.mark.django_db
def test_update_book(book):
    book.title = "Changed"
    book.save()
    book_from_db = Book.objects.get(title="Changed")
    assert book_from_db.title == "Changed"


@pytest.mark.django_db
def test_filter_author(author):
    assert Author.objects.filter(name="Xxx").exists()


@pytest.mark.django_db
def test_update_author(author):
    author.name = "Changed"
    author.save()
    author_from_db = Author.objects.get(name="Changed")
    assert author_from_db.name == "Changed"


@pytest.mark.django_db
def test_BookList_get(book_list):
    client = Client()
    url = reverse('list_books')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], SearchForm)
    assert response.context['list_books'].count() == len(book_list)
    for book in book_list:
        assert book in response.context['list_books']


@pytest.mark.django_db
def test_UpdateViewBook_get(book):
    client = Client()
    url = reverse('update_book', args=(book.id,))
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_UpdateViewBook_post(book):
    client = Client()
    url = reverse('update_book', args=(book.id,))
    data = {
        'title': 'New title',
        }
    response = client.post(url, data)
    breakpoint()
    Book.objects.get(title='New title')

