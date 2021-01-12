# Generated by Django 3.1.5 on 2021-01-12 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('internal', 'Internal'), ('student', 'Student'), ('college-student', 'College Student'), ('junior', 'Junior'), ('company', 'Company'), ('university', 'University'), ('other', 'Other')], default='internal', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
    ]
