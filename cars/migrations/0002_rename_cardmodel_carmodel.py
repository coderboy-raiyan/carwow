# Generated by Django 4.2.7 on 2023-12-15 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CardModel',
            new_name='CarModel',
        ),
    ]
