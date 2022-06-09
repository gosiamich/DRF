import os
import sys
import pytest
from faker import Faker
from rest_framework.test import APIClient

from rest_api_app.models import Book, Author

sys.path.append(os.path.dirname(__file__))
faker = Faker("pl_PL")


@pytest.fixture
def client():
    client = APIClient()
    return client

@pytest.fixture
def book():
    return Book.objects.create(title="Title")

@pytest.fixture
def author():
    return Author.objects.create(name="jan kowalski")

