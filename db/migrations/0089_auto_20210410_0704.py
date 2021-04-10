# Generated by Django 3.1.5 on 2021-04-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0088_auto_20210408_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='company',
            name='branches',
            field=models.ManyToManyField(related_name='companies', to='db.Branch'),
        ),
    ]