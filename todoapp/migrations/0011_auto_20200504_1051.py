# Generated by Django 3.0.5 on 2020-05-04 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0010_todocomments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todocomments',
            options={'ordering': ['-created']},
        ),
    ]
