# Generated by Django 3.2.12 on 2022-06-16 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userdefaultaddress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraddress',
            options={'ordering': ['-updated', '-timestamp']},
        ),
    ]