# Generated by Django 3.2.12 on 2022-05-21 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20220520_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=120)),
                ('address2', models.CharField(blank=True, max_length=120, null=True)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(blank=True, max_length=120, null=True)),
                ('country', models.CharField(max_length=120)),
                ('zipcode', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=120)),
                ('shipping', models.BooleanField(default=True)),
                ('billing', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
