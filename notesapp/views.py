from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

from django.shortcuts import get_object_or_404
from taggit.models import Tag

from notesapp import models
from notesapp import forms

from django.utils import timezone

class CreateNoteView(CreateView, LoginRequiredMixin):
    template_name = 'notesapp/create.html'
    form_class = forms.NoteForm
    model = models.Note
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.edited = timezone.now()
        self.object.save()
        return super().form_valid(form)

class EditNoteView(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'notesapp/view_detail.html'
    template_name = 'notesapp/edit.html'
    form_class = forms.NoteForm
    model = models.Note


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.old_queryset = super().get_queryset()
        self.todo_user = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        user_id = self.todo_user.values('user')

        if ((self.request.user.id) != (user_id.get()['user'])):
             return HttpResponseForbidden() 
                   
        return super().get(request, *args, **kwargs)

class EditStarView(UpdateView,LoginRequiredMixin):
    redirect_field_name = 'notesapp/view_detail.html'
    model = models.Note
    form_class = forms.EditStarForm


    def get_queryset(self):
        self.one_note = super().get_queryset().filter(pk=self.kwargs.get('pk'))
        self.star_value = bool(self.one_note.values('starred'))
        return self.one_note.all()

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.starred = not self.one_note.values()[0]['starred']
        self.object.save()
        return super().form_valid(form)



class AllNotesView(ListView,LoginRequiredMixin):
    template_name = 'notesapp/view_all.html'
    model = models.Note

    def get_queryset(self):

        if self.kwargs.get('option') == 0:#all my
            self.all_notes = super().get_queryset().filter( user__username__iexact=self.request.user.username)
        elif self.kwargs.get('option') == 1:#starred
            self.all_notes = super().get_queryset().filter( starred=True)
        elif self.kwargs.get('option') == 2:#shared
            self.all_notes = super().get_queryset().filter( shared_users_str__isnull=False, 
                                                            shared_users_str__contains=self.request.user.username)

        return self.all_notes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_notes'] = self.all_notes.all()
        context['option'] = self.kwargs.get('option')
        return context


class ShowNoteView(ListView,LoginRequiredMixin):
    template_name = 'notesapp/view_detail.html'
    model = models.Note

    def get_queryset(self):
        self.note_detail = super().get_queryset().filter(pk__iexact=self.kwargs.get('pk'))
        self.shared = super().get_queryset().filter(shared_users_str__contains=self.request.user.username,pk__iexact=self.kwargs.get('pk'))
        return self.note_detail.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_note'] = self.note_detail
        context['shared_note'] = self.shared
        return context


class NotesTagView(ListView,LoginRequiredMixin):
    template_name = 'notesapp/tag_view_detail.html'
    model = models.Note

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('tag'))
        self.notes_tag_list = super().get_queryset().filter(user__username__iexact=self.request.user.username,tags__in=[tag])
        return self.notes_tag_list.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes_list'] = self.notes_tag_list.all()
        context['tag_name'] = self.kwargs.get('tag')
        return context

class DeleteNote(DeleteView,LoginRequiredMixin):
    model = models.Note

    def get_success_url(self, **kwargs): 
        return reverse('notes_app:allnotes', kwargs={'option':0})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

class SearchNoteView(ListView,LoginRequiredMixin):
    template_name = 'notesapp/search_results.html'
    model = models.Note

    def get_queryset(self):
        self.notes_tag_list = super().get_queryset().filter(title__icontains=self.kwargs.get('phrase'))
        return self.notes_tag_list.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes_list'] = self.notes_tag_list.all()
        context['search_phrase'] = self.kwargs.get('phrase')
        return context