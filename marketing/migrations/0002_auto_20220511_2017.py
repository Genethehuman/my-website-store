# Generated by Django 3.2.12 on 2022-05-11 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marketingmessage',
            old_name='end_date',
            new_name='enddate',
        ),
        migrations.RenameField(
            model_name='marketingmessage',
            old_name='start_date',
            new_name='startdate',
        ),
    ]
