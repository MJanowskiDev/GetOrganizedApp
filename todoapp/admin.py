from django.contrib import admin
from todoapp import models
# Register your models here.
admin.site.register(models.ToDo)
admin.site.register(models.ToDoComments)