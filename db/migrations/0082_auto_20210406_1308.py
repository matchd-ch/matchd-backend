# Generated by Django 3.1.5 on 2021-04-06 13:08
from django.db import migrations
from django.db import connection
from db.models import Company


def move_branch(apps, schema_editor):
    cursor = connection.cursor()
    companies = Company.objects.raw("SELECT * FROM db_company")

    for company in companies:
        branch_id = getattr(company, 'branch_id', None)
        if branch_id is None:
            continue
        query = f"INSERT INTO `db_company_branches` (`{company.id}`, `{branch_id}`) VALUES (%i, %i);"
        cursor.execute(query)


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0081_company_branches'),
    ]

    operations = [migrations.RunPython(move_branch, migrations.RunPython.noop)]
