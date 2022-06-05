from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publicate_year = models.IntegerField(null=True)
    pages = models.IntegerField(null=True)
    isbn_number = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=64, null=True)
    cover = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return f'/update_book/{self.id}/'
