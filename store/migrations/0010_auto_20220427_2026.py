# Generated by Django 3.2.12 on 2022-04-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_variation_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='item',
        ),
        migrations.AddField(
            model_name='variation',
            name='item',
            field=models.ManyToManyField(null=True, to='store.Item'),
        ),
    ]