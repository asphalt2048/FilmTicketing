# Generated by Django 5.0.3 on 2024-06-29 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='name',
            new_name='title',
        ),
    ]
