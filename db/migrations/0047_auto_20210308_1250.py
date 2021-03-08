# Generated by Django 3.1.5 on 2021-03-08 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0046_expectation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expectation',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='jobposting',
            name='expectations',
            field=models.ManyToManyField(to='db.Expectation'),
        ),
    ]
