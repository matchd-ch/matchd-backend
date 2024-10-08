# Generated by Django 5.0.6 on 2024-09-10 13:52

import wagtail.images.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0119_alter_company_benefits_alter_company_branches_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrendition',
            name='file',
            field=wagtail.images.models.WagtailImageField(
                height_field='height',
                storage=wagtail.images.models.get_rendition_storage,
                upload_to=wagtail.images.models.get_rendition_upload_to,
                width_field='width'),
        ),
    ]