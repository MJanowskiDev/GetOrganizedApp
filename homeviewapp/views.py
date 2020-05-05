from django.views.generic import ListView
from todoapp import models
from taggit.models import Tag

class HomeView(ListView):
    template_name = 'homeviewapp/home.html'
    model = models.ToDo

    def get_queryset(self):
        self.items = super().get_queryset().filter(user__username__iexact=self.request.user.username)
        return self.items.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tags_ids = []
        
        for x in self.items.values_list('tags', flat = True).all():
            if x != None:
                if not(x in user_tags_ids):
                    user_tags_ids.append(x)

        context['todos_unique_tags'] = Tag.objects.filter(id__in = user_tags_ids)
        context['logged_user'] = self.request.user.username
        
        return context