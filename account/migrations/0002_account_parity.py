# Generated by Django 2.2.4 on 2019-08-14 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='parity',
            field=models.IntegerField(default=0),
        ),
    ]