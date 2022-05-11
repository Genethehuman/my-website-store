# Generated by Django 3.2.12 on 2022-04-25 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_variation_category'),
        ('cart', '0016_cartitem_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, null=True, to='store.Variation'),
        ),
    ]
