import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_api_app.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics



class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
                "title": ["icontains"],
                "authors": ["icontains"],
                "publicate_year": ["iexact", "gte", "lte"],
            }


class GenericBookList(generics.ListCreateAPIView):
    """
      List all books, or create a new book.
      """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class GenericBookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
       Retrieve, update or delete a book instance.
       """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
      This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions
      """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_class = BookFilter


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions

    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']




