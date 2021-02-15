# Generated by Django 3.1.5 on 2021-02-08 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0022_student_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='field_of_study',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='graduation',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='school_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
