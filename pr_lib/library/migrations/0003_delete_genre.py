# Generated by Django 4.2.16 on 2024-12-05 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_genre_book_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
