# Generated by Django 3.1.5 on 2021-02-08 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0025_auto_20210208_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='job_from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='job_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='db.joboption'),
        ),
        migrations.AddField(
            model_name='student',
            name='job_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='db.jobposition'),
        ),
        migrations.AddField(
            model_name='student',
            name='job_to_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
