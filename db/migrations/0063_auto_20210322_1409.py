# Generated by Django 3.1.5 on 2021-03-22 13:59
from django.contrib.auth import get_user_model
from django.db import migrations

from db.models import ProfileType


def move_profile_state(apps, schema_editor):
    users = get_user_model().objects.all()

    for user in users:
        if user.type in ProfileType.valid_company_types():
            user.company.state = user.state
            user.company.profile_step = user.profile_step
            user.company.save()
        elif user.type in ProfileType.valid_student_types():
            user.student.state = user.state
            user.student.profile_step = user.profile_step
            user.student.save()


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0062_auto_20210322_1409'),
    ]

    operations = [
        migrations.RunPython(move_profile_state, migrations.RunPython.noop),
    ]
