import django_filters
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, renderers
from rest_api_app.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import permissions


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


class BookListApi(APIView):
    """
      List all books, or create a new book.
      """
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookDetail(APIView):
    """
    Retrieve, update or delete a book instance.
    """
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        author = self.get_object()
        return Response(author.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)