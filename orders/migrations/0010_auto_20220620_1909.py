# Generated by Django 3.2.12 on 2022-06-20 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_useraddress_options'),
        ('orders', '0009_auto_20220620_1859'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user_biling',
            new_name='user_billing',
        ),
        migrations.AlterField(
            model_name='order',
            name='user_shipping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_shipping', to='accounts.useraddress'),
        ),
    ]
