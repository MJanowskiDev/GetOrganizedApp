from django.forms import Form
from django import forms

class SearchForm(Form):

    search_phrase_field = forms.CharField(label='', 
widget=forms.TextInput(attrs={'placeholder': 'Fraza wyszukiwania', 'autocomplete':'off'}))