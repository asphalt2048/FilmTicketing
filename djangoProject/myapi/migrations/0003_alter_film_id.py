# Generated by Django 5.0.3 on 2024-06-30 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_rename_name_film_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='ID',
            field=models.IntegerField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
