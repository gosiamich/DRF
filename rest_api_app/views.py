import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

# Create your views here.
from django.views.generic import UpdateView, CreateView

from rest_api_app.forms import SearchForm, ApiImportBookForm
from rest_api_app.models import Book, Author


class Index(View):
    def get(self, request):
        return render(request, 'rest_api_app/index.html', {'w': books()})


def books():
    url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
    response = requests.get(url)
    book = response.json()
    data = book.get('items')
    list = []
    for book in data:
        list.append(book)

    print(list)
    return data


class BookList(View):
    def get(self, request):
        form = SearchForm()
        books = Book.objects.all()
        return render(request, 'rest_api_app/table.html', {'books': books, 'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        books = Book.objects.all()
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            language = form.cleaned_data['language']
            year_from = form.cleaned_data['year_from']
            year_to = form.cleaned_data['year_to']
            if title:
                books = books.filter(title__icontains=title)
            if author:
                books = books.filter(author__icontains=author)
            if language:
                books = books.filter(language__startswith=language)
            if year_to:
                books = books.filter(publicate_year__lte=year_to)
            if year_from:
                books = books.filter(publicate_year__gte=year_from)
            return render(request, 'rest_api_app/table.html', {'books': books, 'form': form})
        return render(request, 'rest_api_app/table.html', {'books': books, 'form': form})



class UpdateViewBook(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('list_books')
    template_name = 'rest_api_app/form.html'

class CreateViewBook(CreateView):
    model = Author
    fields = ['name']
    success_url = reverse_lazy('list_books')
    template_name = 'rest_api_app/form.html'


def books():
    url = url='https://www.googleapis.com/books/v1/volumes?q={}'
    search = 'Hobbit'
    search_data = requests.get(url.format(search)).json()
    items = search_data.get('items')
    print(search_data)
    return items


class ApiImportBook(View):
    def get(self, request):
        form = ApiImportBookForm()
        message = 'Import book from Google Api'
        return render(request, 'rest_api_app/form.html', {'form': form, 'message': message})

    def post(self, request):
        form = ApiImportBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = url = 'https://www.googleapis.com/books/v1/volumes?q={}'
            search_data = requests.get(url.format(title)).json()
            items = search_data.get('items')
            books = []
            for item in items:
                title=item['volumeInfo']['title']
                authors=item['volumeInfo'].get('authors')
                publishedDate=item['volumeInfo']['publishedDate'][0:4]
                ISBN=item['volumeInfo'].get('industryIdentifiers')
                pageCount=item['volumeInfo'].get('pageCount')
                imageLinks=item['volumeInfo'].get('imageLinks')
                language=item['volumeInfo']['language']
                book, created = Book.objects.get_or_create(title=title,
                                                           publicate_year=publishedDate,
                                                           pages=pageCount,
                                                           language=language)
                for name in authors:
                    name = name.strip()
                    author, created = Author.objects.get_or_create(name=name)
                    book.authors.add(author)
                for no in ISBN:
                    if no['type'] == ['ISBN_10']:
                        isbn = no['identifier']
                        book.isbn_number = isbn
                # book.cover =imageLinks.get('smallThumbnail')
                book.save()
                books.append(book)
            print(search_data)
            return render(request, 'rest_api_app/form.html', {'form': form, 'books': books})



