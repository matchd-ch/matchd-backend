# Generated by Django 3.1.5 on 2021-06-05 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0106_projectposting'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.company'),
        ),
        migrations.AddField(
            model_name='match',
            name='project_posting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.projectposting'),
        ),
        migrations.AlterField(
            model_name='match',
            name='job_posting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.jobposting'),
        ),
        migrations.AlterField(
            model_name='match',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.student'),
        ),
    ]