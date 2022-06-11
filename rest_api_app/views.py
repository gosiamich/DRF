import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

# Create your views here.
from django.views.generic import UpdateView, CreateView

from rest_api_app.forms import SearchForm, ApiImportBookForm
from rest_api_app.models import Book, Author


def books():
    url = url = 'https://www.googleapis.com/books/v1/volumes?q={}'
    search = 'Python'
    search_data = requests.get(url.format(search)).json()
    items = search_data.get('items')
    list = []
    result = []
    for book in items:
        list.append(book)
        result.append(book['volumeInfo']['title'])
    return result


class Index(View):
    def get(self, request):
        return render(request, 'rest_api_app/index.html', {'w': books()})

class CreateViewBook(CreateView):
    model = Book
    fields = ['title', 'authors', 'publicate_year', 'pages', 'isbn_number', 'cover', 'language']
    success_url = reverse_lazy('list_books')
    template_name = 'rest_api_app/form.html'



class BookList(View):
    def get(self, request):
        form = SearchForm()
        list_books = Book.objects.all()
        paginator = Paginator(list_books, 5)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        return render(request, 'rest_api_app/table.html', {'books': books, 'list_books': list_books, 'form': form})

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
            paginator = Paginator(books, 5)
            page = request.GET.get('page')
            list = paginator.get_page(page)
            return render(request, 'rest_api_app/table.html', {'books': list, 'form': form})
        return render(request, 'rest_api_app/table.html', {'books': books, 'form': form})


class UpdateViewBook(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('list_books')
    template_name = 'rest_api_app/form.html'


class CreateViewAuthor(CreateView):
    model = Author
    fields = ['name']
    success_url = reverse_lazy('list_books')
    template_name = 'rest_api_app/form.html'


class ApiImportBook(View):
    def get(self, request):
        form = ApiImportBookForm()
        message = 'Import book from Google Api'
        return render(request, 'rest_api_app/form.html', {'form': form, 'message': message})

    def post(self, request):
        form = ApiImportBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data.get('author')
            publisher = form.cleaned_data.get('publisher')
            subject = form.cleaned_data.get('subject')
            isbn = form.cleaned_data.get('isbn')
            lccn = form.cleaned_data.get('lccn')
            oclc = form.cleaned_data.get('oclc')
            input_data = ''
            if title:
                input_data += f'{title}+intitle&'
            if author:
                input_data += f'{author}+inauthor&'
            if publisher:
                input_data += f'{publisher}+inpublisher&'
            if subject:
                input_data += f'{subject}+subject&'
            if isbn:
                input_data += f'{isbn}+isbn&'
            if lccn:
                input_data += f'{lccn}+lccn&'
            if oclc:
                input_data += f'+{oclc}intitle&'

            url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType=books'
            search_data = requests.get(url.format(input_data)).json()
            items = search_data.get('items')
            # breakpoint()
            books = []
            for item in items:
                title = item['volumeInfo']['title']
                authors = item['volumeInfo'].get('authors', [])
                publishedDate = item['volumeInfo']['publishedDate'][0:4]
                ISBN = item['volumeInfo'].get('industryIdentifiers')
                pageCount = item['volumeInfo'].get('pageCount')
                imageLinks = item['volumeInfo'].get('imageLinks')
                language = item['volumeInfo']['language']
                book, created = Book.objects.get_or_create(title=title,
                                                           publicate_year=publishedDate,
                                                           pages=pageCount,
                                                           language=language)
                # breakpoint()
                if len(authors) > 0:
                    for name in authors:
                        if len(Author.objects.filter(name=name)) < 1:
                            author = Author.objects.create(name=name)
                            book.authors.add(author)
                        else:
                            book.authors.add(Author.objects.get(name=name))
                for no in ISBN:
                    if no['type'] == ['ISBN_13']:
                        isbn = no['identifier']
                        book.isbn_number = isbn

                book.cover = imageLinks.get('smallThumbnail')
                book.save()
                books.append(book)
            print(search_data)
            return render(request, 'rest_api_app/form.html', {'form': form, 'books': books})
