from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import ToDo
from django.forms import BooleanField
import django.forms as forms

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ['username','password1','password2']
        model = get_user_model()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class TodoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['placeholder'] = 'Lista hashtagów oddzielona przecinkami'

        self.fields['title'].widget.attrs['autocomplete'] = 'off'
        self.fields['tags'].widget.attrs['autocomplete'] = 'off'
        self.fields['memo'].widget.attrs['autocomplete'] = 'off'
    class Meta:
        model = ToDo
        fields = ['title', 'tags', 'memo', 'important']

        labels = {  'title':'Nazwa',
            'memo':'Opis',
            'important':'Oznacz jako pilne',
            'tags':'Hashtagi'}

class EditTodoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['placeholder'] = 'Lista hashtagów oddzielona przecinkami'

        self.fields['title'].widget.attrs['autocomplete'] = 'off'
        self.fields['tags'].widget.attrs['autocomplete'] = 'off'
        self.fields['memo'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = ToDo
        fields = ['title', 'tags', 'memo', 'important']

        labels = {  'title':'Nazwa ',
            'memo':'Opis ',
            'important':'Oznacz jako pilne',
            'tags':'Hashtagi'}

        widgets = {
            'memo': forms.Textarea(attrs={'rows':2})
        }

class MakeComplete(ModelForm):
    class Meta:
        model = ToDo
        fields = ['done', 'datecompleted']

        
