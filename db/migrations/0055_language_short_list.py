# Generated by Django 3.1.5 on 2021-03-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0054_jobpostinglanguagerelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='short_list',
            field=models.BooleanField(default=False),
        ),
    ]
