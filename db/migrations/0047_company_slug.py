# Generated by Django 3.1.5 on 2021-03-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0046_auto_20210309_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
