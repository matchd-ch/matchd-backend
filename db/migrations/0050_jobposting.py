# Generated by Django 3.1.5 on 2021-03-04 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0049_auto_20210310_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
                ('workload', models.CharField(blank=True, max_length=255, null=True)),
                ('job_from_date', models.DateField()),
                ('job_to_date', models.DateField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('form_step', models.IntegerField(default=2)),
                ('company',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.company')),
                ('job_option',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.joboption')),
            ],
        ),
    ]
