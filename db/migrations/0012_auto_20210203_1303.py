# Generated by Django 3.1.5 on 2021-02-03 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_languageniveau'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='languageniveau',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
