# Generated by Django 3.2.12 on 2022-04-02 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_item_size'),
        ('cart', '0002_auto_20220331_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='store.Item'),
        ),
    ]
