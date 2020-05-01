
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView,TemplateView,FormView,DetailView,ListView, UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from todoapp import forms
from django.contrib.auth import views as auth_views
from .forms import TodoForm,EditTodoForm,MakeComplete
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model, get_user
User_model = get_user_model()

from django.utils import timezone

from django.http import HttpResponseNotFound

from taggit.models import Tag

from django.shortcuts import get_object_or_404


class SignUpView(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('home') #after registration and hit signup button
    template_name = 'todoapp/signupuser.html'

class SiteLoginView(auth_views.LoginView):
    template_name = 'todoapp/login.html'
    success_url = reverse_lazy("home")


class SiteLogoutView(auth_views.LogoutView):
    template_name = 'todoapp/logout.html'

class TagView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/tagview.html'
    model = models.ToDo

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('tag'))
        self.todo_tag = super().get_queryset().filter(user__username__iexact=self.kwargs.get('username'),tags__in=[tag])
        return self.todo_tag.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_tag'] = self.todo_tag.all()
        context['tag_name'] = self.kwargs.get('tag')
        return context

class TodosView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/currenttodos.html'
    model = models.ToDo

    def get_queryset(self):
        self.todo_user = super().get_queryset().filter(user__username__iexact=self.kwargs.get('username'),done=False)#User_model.objects.prefetch_related("todo").filter(user=self.kwargs.get("user"))
        return self.todo_user.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_user'] = self.todo_user.all()
        return context

class DoneTodosView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/donetodos.html'
    model = models.ToDo

    def get_queryset(self):
        self.todo_user = super().get_queryset().filter(user__username__iexact=self.kwargs.get('username'), done=True)
        return self.todo_user.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_user'] = self.todo_user.all()
        return context

class HomeView(TemplateView):
    template_name = 'todoapp/home.html'


class CreateTodoView(CreateView):

    template_name = 'todoapp/create.html'
    form_class = TodoForm


    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    
class EditTodoView(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'todoapp/current.html'
    template_name = 'todoapp/edit.html'
    form_class = EditTodoForm
    model = models.ToDo

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.old_queryset = super().get_queryset()
        self.todo_user = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        user_id = self.todo_user.values('user')

        if ((self.request.user.id) != (user_id.get()['user'])):
             return HttpResponseNotFound('<h1>Page not found</h1>') 
                   
        return super().get(request, *args, **kwargs)


class DeleteTodoView(DeleteView,LoginRequiredMixin):
    model = models.ToDo

    def get_success_url(self, **kwargs): 
        return reverse('currenttodos', kwargs={'username': self.kwargs.get('user')})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

class CompleteTodoView(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'todoapp/current.html'
    form_class = MakeComplete
    model = models.ToDo


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.old_queryset = super().get_queryset()
        self.todo_user = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        user_id = self.todo_user.values('user')

        if ((self.request.user.id) != (user_id.get()['user'])):
             return HttpResponseNotFound('<h1>Page not found</h1>') 
                   
        return super().get(request, *args, **kwargs)

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.done = True
        self.object.datecompleted = timezone.now()
        self.object.save()
        return super().form_valid(form)


class RevertComplete(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'todoapp/current.html'
    form_class = MakeComplete
    model = models.ToDo


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.old_queryset = super().get_queryset()
        self.todo_user = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        user_id = self.todo_user.values('user')

        if ((self.request.user.id) != (user_id.get()['user'])):
            return HttpResponseNotFound('<h1>Page not found</h1>') 
                
        return super().get(request, *args, **kwargs)

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.done = False
        self.object.save()
        return super().form_valid(form)       