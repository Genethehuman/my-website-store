# Generated by Django 3.2.12 on 2022-03-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name_plural': 'zhopki'},
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(auto_created=True, unique=True),
        ),
    ]
