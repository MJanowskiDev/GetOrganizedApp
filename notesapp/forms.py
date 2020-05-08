from django.forms import ModelForm
from notesapp import models

from django_summernote.widgets import SummernoteWidget

class NoteForm(ModelForm):

    #foo = SummernoteFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['placeholder'] = 'Lista hashtagów oddzielona przecinkami'
        self.fields['shared_users_str'].widget.attrs['placeholder'] = 'Lista użytkowników oddzielona przecinkami'


        self.fields['title'].widget.attrs['autocomplete'] = 'off'
        self.fields['tags'].widget.attrs['autocomplete'] = 'off'
        self.fields['body'].widget.attrs['autocomplete'] = 'off'
        self.fields['body'].widget = SummernoteWidget()

    class Meta:
        model = models.Note
        
        fields = [  'title', 
                    'tags', 
                    'body', 
                    'starred',
                    'shared_users_str']

        labels = {  'title':'Tytuł',
                    'body':'Treść',
                    'starred':'Oznaczone gwiazdką',
                    'tags':'Hashtagi',
                    'shared_users_str':'Udostępnione dla'}

class EditStarForm(ModelForm):


    class Meta:
        model = models.Note
        fields = ['starred']
