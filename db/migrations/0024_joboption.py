# Generated by Django 3.1.5 on 2021-02-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0023_auto_20210208_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOption',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type',
                 models.CharField(choices=[('date_from', 'Date from'),
                                           ('date_range', 'Date range')],
                                  max_length=255)),
            ],
        ),
    ]
