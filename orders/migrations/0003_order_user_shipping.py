# Generated by Django 3.2.12 on 2022-06-16 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_useraddress_options'),
        ('orders', '0002_auto_20220428_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_shipping',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.useraddress'),
        ),
    ]
