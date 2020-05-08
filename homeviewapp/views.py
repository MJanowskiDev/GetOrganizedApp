from django.views.generic import ListView
from todoapp import models
from notesapp import models as notes_models
from taggit.models import Tag
from homeviewapp import forms
from django.urls import  reverse
from django.http import HttpResponseRedirect


class HomeView(ListView):
    template_name = 'homeviewapp/home.html'
    model = models.ToDo

    #get unique tags occurence in queryset and returns list of tag objects
    def get_unique_tags(self, query, tags_name = 'tags'):
        user_tags_ids = []
        
        for x in query.values_list('tags', flat = True).all():
            if x != None:
                if not(x in user_tags_ids):
                    user_tags_ids.append(x)
        return user_tags_ids


    def get_queryset(self):
        self.items = super().get_queryset().filter(user__username__iexact=self.request.user.username)
        return self.items.all()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.notes_tags = notes_models.Note.objects.filter(user__username__iexact=self.request.user.username)

        context['todos_unique_tags'] = Tag.objects.filter(id__in = self.get_unique_tags(self.items))
        context['notes_unique_tags'] = Tag.objects.filter(id__in = self.get_unique_tags(self.notes_tags))
        context['logged_user'] = self.request.user.username
        context['form'] = forms.SearchForm()
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = forms.SearchForm(request.POST)

            if form.is_valid():
                search_string=form.cleaned_data['search_phrase_field']
                return HttpResponseRedirect(reverse('notes_app:searchnote', kwargs={'phrase':search_string}))


