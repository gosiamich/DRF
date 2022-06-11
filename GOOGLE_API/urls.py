"""GOOGLE_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_api_app.views import Index, BookList, UpdateViewBook, ApiImportBook, CreateViewAuthor, CreateViewBook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('books/', BookList.as_view(), name='list_books'),
    path('update_book/<int:pk>/', UpdateViewBook.as_view(), name='update_book'),
    path('import_book/', ApiImportBook.as_view(), name='import_book'),
    path('create_author', CreateViewAuthor.as_view(), name='create_author'),
    path('create_book/', CreateViewBook.as_view(), name='create_book'),
    path('',include('API.urls'))
]
