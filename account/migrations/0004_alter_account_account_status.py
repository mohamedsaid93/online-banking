# Generated by Django 4.2.4 on 2023-10-03 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_kyc_account_kyc_identity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_status',
            field=models.CharField(choices=[('active', 'Active'), ('in active', 'Inactive')], default='in-active', max_length=100),
        ),
    ]