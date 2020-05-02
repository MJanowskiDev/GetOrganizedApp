# Generated by Django 3.0.5 on 2020-05-02 04:35

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('todoapp', '0007_todo_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Lista hashtagów oddzielona przecinkami', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
