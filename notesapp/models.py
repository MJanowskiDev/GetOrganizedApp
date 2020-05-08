from django.db import models
from taggit.managers import TaggableManager

from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

class Note(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    edited = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note')
    shared_users_str = models.CharField(max_length=250, blank = True)
    tags = TaggableManager(help_text='Lista hashtagów oddzielona przecinkami', blank = True)
    starred = models.BooleanField(default = False)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created']

    
    def get_absolute_url(self):
        return reverse('notes_app:allnotes', kwargs={ 'option':0})