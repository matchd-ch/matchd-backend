# Generated by Django 3.1.5 on 2021-04-06 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0085_remove_student_job_position'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobPosition',
        ),
    ]
