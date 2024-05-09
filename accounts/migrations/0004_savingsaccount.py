# Generated by Django 5.0.4 on 2024-05-09 01:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_bonusaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingsAccount',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.account')),
            ],
            bases=('accounts.account',),
        ),
    ]
