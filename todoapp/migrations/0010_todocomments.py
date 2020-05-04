# Generated by Django 3.0.5 on 2020-05-04 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0009_todo_shared_users_str'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_todo', to='todoapp.ToDo')),
            ],
        ),
    ]
