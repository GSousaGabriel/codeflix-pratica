# Generated by Django 5.2 on 2025-04-10 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genre_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='categories',
            new_name='categories_ids',
        ),
    ]
