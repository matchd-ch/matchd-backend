# Generated by Django 3.1.5 on 2021-01-12 14:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20210112_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex='CHE-[0-9]{3}.[0-9]{3}.[0-9]{3}')])),
                ('name', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
