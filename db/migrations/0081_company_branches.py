# Generated by Django 3.1.5 on 2021-04-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0080_company_cultural_fits'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='branches',
            field=models.ManyToManyField(blank=True, null=True, related_name='companies', to='db.Branch'),
        ),
    ]
