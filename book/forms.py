# forms.py
from django import forms

class BookSearchForm(forms.Form):
    book_name = forms.CharField(max_length=200, label='Enter Book Name')
