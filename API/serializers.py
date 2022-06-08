from rest_framework import serializers
from rest_api_app.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'publicate_year', 'pages', 'isbn_number', 'cover', 'language']


class BookField(serializers.RelatedField):
    def to_representation(self, book):
        return book.title

class AuthorSerializer(serializers.ModelSerializer):
    book_set = BookField(read_only=True, many=True)

    class Meta:
        model = Author
        fields = ['name', 'book_set']
