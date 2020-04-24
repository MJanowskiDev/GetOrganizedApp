from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import ToDo

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ['username','password1','password2']
        model = get_user_model()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class TodoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'important']

class EditTodoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'important' ]

class MakeComplete(ModelForm):
    class Meta:
        model = ToDo
        fields = ['done', 'datecompleted']
