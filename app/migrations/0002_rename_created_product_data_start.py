# Generated by Django 4.2.10 on 2024-03-01 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='created',
            new_name='data_start',
        ),
    ]