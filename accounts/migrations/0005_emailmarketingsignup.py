# Generated by Django 3.2.12 on 2022-05-20 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_hashkey_emailconfirmed_activation_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMarketingSignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
    ]