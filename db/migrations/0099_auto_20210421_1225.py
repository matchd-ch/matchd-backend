# Generated by Django 3.1.5 on 2021-04-21 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0098_auto_20210421_1222'),
    ]

    operations = [
        migrations.RunSQL(
            "UPDATE db_jobposting SET date_published = date_created WHERE state = 'public';",
            migrations.RunSQL.noop)
    ]
