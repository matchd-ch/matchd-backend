# Generated by Django 3.1.5 on 2021-03-15 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0057_jobposting_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.employee'),
        ),
    ]
