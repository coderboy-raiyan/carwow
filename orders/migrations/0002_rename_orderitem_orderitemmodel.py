# Generated by Django 4.2.7 on 2023-12-15 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_brandmodel_slug'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='OrderItemModel',
        ),
    ]
