# Generated by Django 3.1.5 on 2021-03-30 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0072_student_soft_skills'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expectation',
            new_name='JobRequirement',
        ),
    ]
