import pytest
from django.contrib.auth.models import User

from rest_api_app.models import Book, Author

@pytest.fixture
def user():
    user = User.objects.create_user(username='gosia', password='gosia', is_superuser=True)
    return user

@pytest.fixture
def book():
    return Book.objects.create(title="Books")

@pytest.fixture
def author():
    return Author.objects.create(name="Xxx")

@pytest.fixture
def book_list():
    list =[]
    for i in range(3):
        book = Book.objects.create(title=i)
        list.append(book)
    return list