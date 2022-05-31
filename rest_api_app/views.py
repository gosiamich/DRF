import requests
from django.shortcuts import render
from django.views import View


# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, 'rest_api_app/index.html', {'w': books()})

def books():
    url='https://www.googleapis.com/books/v1/volumes?q=Hobbit'
    response = requests.get(url)
    book = response.json()
    data = book.get('items')
    list =[]
    for book in data:
        list.append(book['volumeInfo']['title'])

    print(list)
    return data