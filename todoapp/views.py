
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView,FormView,ListView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponseNotFound, HttpResponseForbidden
from taggit.models import Tag
from django.shortcuts import get_object_or_404

from .forms import TodoForm, MakeCompleteForm, CommentBodyForm
from todoapp import models


class TagView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/tagview.html'
    model = models.ToDo

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('tag'))
        self.todo_tag = super().get_queryset().filter(user__username__iexact=self.kwargs.get('username'),tags__in=[tag])
        self.shared = self.todo_tag.filter(shared_users_str__isnull=False, shared_users_str__contains=self.request.user.username)
        return self.todo_tag.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_tag'] = self.todo_tag.all()
        context['tag_name'] = self.kwargs.get('tag')
        context['shared_field'] = self.shared
        return context

class TodosView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/currenttodos.html'
    model = models.ToDo

    def get_queryset(self):

        if self.kwargs.get('shared'):
            self.todo_user = super().get_queryset().filter(shared_users_str__isnull=False, shared_users_str__contains=self.kwargs.get('username'))
        else:
            self.todo_user = super().get_queryset().filter( user__username__iexact=self.kwargs.get('username'),
                                                            done=bool(self.kwargs.get('done')))
        return self.todo_user.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_user'] = self.todo_user.all()
        context['done_field'] = self.kwargs.get('done')
        context['shared_field'] = self.kwargs.get('shared')
        return context





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
    form_class = TodoForm
    model = models.ToDo

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.old_queryset = super().get_queryset()
        self.todo_user = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        user_id = self.todo_user.values('user')

        if ((self.request.user.id) != (user_id.get()['user'])):
             return HttpResponseNotFound('<h1>Page not found</h1>') 
                   
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteTodoView(DeleteView,LoginRequiredMixin):
    model = models.ToDo

    def get_success_url(self, **kwargs): 
        return reverse('todo_app:currenttodos', kwargs={'username': self.kwargs.get('user'),'done':0, 'shared':0})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

class CompleteTodoView(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'todoapp/current.html'
    form_class = MakeCompleteForm
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
    form_class = MakeCompleteForm
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


class ShowTaskView(ListView,LoginRequiredMixin):
    template_name = 'todoapp/showtask.html'
    model = models.ToDo

    def get_queryset(self):
        self.todo_detail = super().get_queryset().filter(pk__iexact=self.kwargs.get('pk'))
        self.shared = super().get_queryset().filter(shared_users_str__isnull=False, shared_users_str__contains=self.request.user.username,pk__iexact=self.kwargs.get('pk'))
        return self.todo_detail.all()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_todo'] = self.todo_detail
        context['shared_field'] = self.shared
        context['comment_form'] = CommentBodyForm()
        context['comments'] = models.ToDoComments.objects.filter(todo_id=self.kwargs.get('pk')).values()
        return context


class ToDoCommentView(FormView, LoginRequiredMixin):
    template_name = 'todoapp/comment.html'
    form_class = CommentBodyForm

    def get_success_url(self, **kwargs): 
        return reverse('todo_app:showtask', kwargs={'pk':self.kwargs.get('pk')})

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.username = self.request.user.username
        self.object.todo = models.ToDo.objects.get(id = self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)
