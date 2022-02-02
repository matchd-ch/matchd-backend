# Generated by Django 3.1.5 on 2021-03-22 13:59
from django.contrib.auth import get_user_model
from django.db import migrations

from db.models import ProfileType, Student
from django.db import connection


def move_profile_state(apps, schema_editor):
    cursor = connection.cursor()
    users = get_user_model().objects.raw('SELECT * FROM db_user;')

    for user in users:
        state = user.__dict__.get('state')
        step = user.__dict__.get('profile_step')
        if getattr(user, 'type') in ProfileType.valid_company_types():
            company_id = user.__dict__.get('company_id')
            query = "UPDATE db_company SET state='%s', profile_step=%s WHERE id=%s;" % (
                state, str(step), str(company_id))
            cursor.execute(query)
        elif getattr(user, 'type') in ProfileType.valid_student_types():
            query = 'SELECT * FROM db_student WHERE user_id=%s;' % getattr(user, 'id')
            student = Student.objects.raw(query)
            query = "UPDATE db_student SET state='%s', profile_step=%s WHERE id=%s;" % (
                state, str(step), str(student[0].id))
            cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0062_auto_20210322_1409'),
    ]

    operations = [
        migrations.RunPython(move_profile_state, migrations.RunPython.noop),
    ]
