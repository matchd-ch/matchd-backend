# Generated by Django 3.1.5 on 2021-02-09 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0021_auto_20210204_1758'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hobby',
            unique_together={('name', 'student')},
        ),
    ]
