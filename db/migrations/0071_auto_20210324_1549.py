# Generated by Django 3.1.5 on 2021-03-24 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0070_auto_20210324_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='soft_skills',
            field=models.ManyToManyField(related_name='companies', to='db.SoftSkill'),
        ),
        migrations.AlterField(
            model_name='company',
            name='benefits',
            field=models.ManyToManyField(related_name='companies', to='db.Benefit'),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_positions',
            field=models.ManyToManyField(related_name='companies', to='db.JobPosition'),
        ),
        migrations.AlterField(
            model_name='student',
            name='skills',
            field=models.ManyToManyField(related_name='students', to='db.Skill'),
        ),
    ]
