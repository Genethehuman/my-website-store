# Generated by Django 3.2.12 on 2022-06-16 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_useraddress_options'),
        ('orders', '0003_order_user_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_biling',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_shipping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.useraddress'),
        ),
    ]
