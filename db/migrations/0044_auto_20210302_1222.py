# Generated by Django 3.1.5 on 2021-03-02 12:22

from django.db import migrations, models

import db.models.video


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0043_auto_20210302_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=db.models.video.get_upload_to, verbose_name='file'),
        ),
    ]
