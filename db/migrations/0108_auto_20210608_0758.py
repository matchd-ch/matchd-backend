# Generated by Django 3.1.5 on 2021-06-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0107_auto_20210605_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='key',
            field=models.CharField(choices=[
                ('student_avatar', 'Student Avatar'), ('student_documents', 'Student Documents'),
                ('company_avatar', 'Company Avatar'), ('company_documents', 'Company Documents'),
                ('student_avatar_fallback', 'Student Avatar fallback'),
                ('company_avatar_fallback', 'Company Avatar fallback'),
                ('project_posting_images', 'Project posting images'),
                ('project_posting_documents', 'Project posting documents'),
                ('project_posting_fallback', 'Project posting fallback')
            ],
                                   max_length=100),
        ),
    ]
