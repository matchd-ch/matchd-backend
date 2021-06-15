# Generated by Django 3.1.5 on 2021-06-02 09:15

from django.db import migrations, models
import django.db.models.deletion
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0105_projecttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPosting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('slug', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('additional_information', models.TextField(max_length=1000)),
                ('website', models.URLField(blank=True, max_length=2048)),
                ('project_from_date', models.DateField(blank=True, null=True)),
                ('form_step', models.IntegerField(default=2)),
                ('state', models.CharField(choices=[('draft', 'Draft'), ('public', 'Public')], default='draft', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_published', models.DateTimeField(null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_postings', to='db.company')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.employee')),
                ('keywords', models.ManyToManyField(related_name='project_postings', to='db.Keyword')),
                ('project_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.projecttype')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_postings', to='db.student')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.topic')),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
    ]
