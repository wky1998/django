# Generated by Django 2.1.5 on 2019-10-15 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='likes',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='category',
            name='views',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
