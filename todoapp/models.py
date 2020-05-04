from django.db import models
from django.contrib import auth
from django.shortcuts import reverse
from taggit.managers import TaggableManager


class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

class ToDo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank = True)
    created = models.DateTimeField(auto_now=True)
    datecompleted = models.DateTimeField(null=True, blank = True)
    important = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, related_name='todo')

    shared_users_str = models.CharField(max_length=250, blank = True)
    tags = TaggableManager(help_text='Lista hashtagów oddzielona przecinkami', blank = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('currenttodos', kwargs={'username': self.user.username, 'done':0, 'shared':0})

    class Meta:
        ordering = ['-created']

class ToDoComments(models.Model):
    todo = models.ForeignKey(to=ToDo, on_delete=models.CASCADE,related_name='comments_todo')
    username = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    body = models.TextField()
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']

