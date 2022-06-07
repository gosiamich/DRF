from django import forms
from django.core.exceptions import ValidationError

from rest_api_app.models import Book





# def check_year(year):
#     if year < 1900 or year > 2022:
#         raise ValidationError('Choose year between 1900-2021')


class SearchForm(forms.Form):
    title = forms.CharField(required=False,label='',widget = forms.TextInput(attrs={'placeholder': 'Title'}))
    author = forms.CharField(required=False,label='',widget = forms.TextInput(attrs={'placeholder': 'Author'}))
    language = forms.CharField(required=False,label='',widget = forms.TextInput(attrs={'placeholder': 'Language'}))
    year_from =forms.IntegerField(required=False, min_value=1900,label='',
                                  # validators=[check_year,],
                                  widget= forms.NumberInput(attrs={'placeholder': 'Published from'}))
    year_to = forms.IntegerField(required=False,max_value=2022,label='',
                                 # validators=[check_year,],
                                  widget= forms.NumberInput(attrs={'placeholder': 'Published to'}))

    def clean(self):
        data = super().clean()
        if not 'year_to' in data:
            return data
        if not 'year_from' in data:
            return data
        breakpoint()
        if data['year_from'] and data['year_to']:
            if data['year_from'] > data['year_to']:
                raise forms.ValidationError('Year from must be smaller than Year to')
        return data


class ApiImportBookForm(forms.Form):
    title = forms.CharField(required=False, label='',
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    author = forms.CharField(required=False, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Author'}))
    publisher = forms.CharField(max_length=128, label='', required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Publisher'}))
    subject = forms.CharField(max_length=64, label='', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    isbn = forms.CharField(min_length=10, max_length=13, label='', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'ISBN'}))
    lccn = forms.CharField(max_length=128, label='', required=False,
                           help_text='Library of Congress Control Number',
                           widget=forms.TextInput(attrs={'placeholder': 'LCCN'}))
    oclc = forms.CharField(max_length=128, label='', required=False,
                           help_text='Online Computer Library Center number',
                           widget=forms.TextInput(attrs={'placeholder': 'OCCN'}))



