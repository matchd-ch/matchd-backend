# Generated by Django 3.1.5 on 2021-03-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0048_auto_20210310_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
