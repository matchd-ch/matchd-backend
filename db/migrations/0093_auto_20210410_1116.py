# Generated by Django 3.1.5 on 2021-04-10 11:02

from django.db import migrations, connection
from django.utils.text import slugify

from db.models import JobPosting


def add_job_posting_slug(apps, schema_editor):
    cursor = connection.cursor()
    job_postings = JobPosting.objects.raw("SELECT * FROM db_jobposting")

    for job_posting in job_postings:
        slug = slugify(job_posting.title)
        query = "UPDATE `db_jobposting` SET slug='%s-%i' WHERE id=%i" % \
                (slug, job_posting.id, job_posting.id)
        cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0092_jobposting_slug'),
    ]

    operations = [
        migrations.RunPython(add_job_posting_slug, migrations.RunPython.noop)
    ]
