# Generated by Django 3.1.5 on 2021-05-17 14:26

from django.db import migrations
from django.db import connection
from db.models import JobPosting


def move_branch(apps, schema_editor):
    cursor = connection.cursor()
    job_postings = JobPosting.objects.raw("SELECT * FROM db_jobposting")

    for job_posting in job_postings:
        branch_id = getattr(job_posting, 'branch_id', None)
        if branch_id is None:
            continue
        query = "INSERT INTO `db_jobposting_branches` (`jobposting_id`, `branch_id`) VALUES (%i, %i);" % \
                (job_posting.id, branch_id)
        cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0101_jobposting_branches'),
    ]

    operations = [migrations.RunPython(move_branch, migrations.RunPython.noop)]
