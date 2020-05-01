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
        self.fields['tags'].widget.attrs['placeholder'] = 'Tagi oddzielone ,'

    class Meta:
        model = ToDo
        fields = ['title', 'tags', 'memo', 'important']

        labels = {  'title':'Nazwa ',
            'memo':'Opis ',
            'important':'Oznacz jako pilne',
            'tags':'Hashtagi'}

        widgets = {
            'memo': forms.Textarea(attrs={'rows':4})
        }

class MakeComplete(ModelForm):
    class Meta:
        model = ToDo
        fields = ['done', 'datecompleted']

        
