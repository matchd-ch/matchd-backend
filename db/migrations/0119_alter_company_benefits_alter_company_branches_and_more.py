# Generated by Django 4.1.10 on 2023-09-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0118_remove_company_profile_step_alter_company_benefits_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='benefits',
            field=models.ManyToManyField(blank=True, related_name='companies', to='db.benefit'),
        ),
        migrations.AlterField(
            model_name='company',
            name='branches',
            field=models.ManyToManyField(blank=True, related_name='companies', to='db.branch'),
        ),
        migrations.AlterField(
            model_name='company',
            name='cultural_fits',
            field=models.ManyToManyField(blank=True, related_name='companies', to='db.culturalfit'),
        ),
        migrations.AlterField(
            model_name='company',
            name='soft_skills',
            field=models.ManyToManyField(blank=True, related_name='companies', to='db.softskill'),
        ),
        migrations.AlterField(
            model_name='student',
            name='cultural_fits',
            field=models.ManyToManyField(blank=True, related_name='students', to='db.culturalfit'),
        ),
        migrations.AlterField(
            model_name='student',
            name='soft_skills',
            field=models.ManyToManyField(blank=True, related_name='students', to='db.softskill'),
        ),
    ]
