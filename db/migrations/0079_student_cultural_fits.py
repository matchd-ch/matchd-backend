# Generated by Django 3.1.5 on 2021-03-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0078_culturalfit'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cultural_fits',
            field=models.ManyToManyField(blank=True, related_name='students', to='db.CulturalFit'),
        ),
    ]
