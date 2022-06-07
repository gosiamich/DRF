from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256)
    authors = models.ManyToManyField(Author)
    publicate_year = models.IntegerField(null=True)
    pages = models.IntegerField(null=True)
    isbn_number = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=64, null=True)
    cover = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return f'/update_book/{self.id}/'

    def all_authors(self):
        return ', '.join([item.name for item in self.authors.all()])

    def show_url(self):
        if self.cover is not None:
            return format_html(f'<a href="{self.cover}">{self.cover}</a>')
        else:
            return ''