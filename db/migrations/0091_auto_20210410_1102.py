# Generated by Django 3.1.5 on 2021-04-10 11:02

from django.db import migrations, connection
from django.utils.text import slugify

from db.models import Student


def add_student_slug(apps, schema_editor):
    cursor = connection.cursor()
    students = Student.objects.all()

    for student in students:
        if student.profile_step >= 5:
            if student.slug is None or student.slug == '':
                query = "UPDATE `db_student` SET slug='%s' WHERE id=%i" % (slugify(student.nickname), student.id)
                cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0090_student_slug'),
    ]

    operations = [
        migrations.RunPython(add_student_slug, migrations.RunPython.noop)
    ]
