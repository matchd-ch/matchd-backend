# Generated by Django 3.2.13 on 2022-07-01 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0108_auto_20210608_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_matchable',
            field=models.BooleanField(default=True),
        ),
    ]