# Generated by Django 3.1.5 on 2021-03-09 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0044_auto_20210308_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='benefit',
            options={'ordering': ('name', 'icon')},
        ),
        migrations.AddField(
            model_name='benefit',
            name='name',
            field=models.CharField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
