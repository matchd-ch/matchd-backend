# Generated by Django 3.2.15 on 2022-08-23 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0112_add_team_size_and_compensation_to_project_posting'),
    ]

    operations = [
        migrations.RenameModel('ProjectPosting', 'Challenge'),
        migrations.RenameModel('OnlineProject', 'OnlineChallenge'),
        migrations.AlterField(
            model_name='attachment',
            name='key',
            field=models.CharField(choices=[('student_avatar', 'Student Avatar'),
                                            ('student_documents', 'Student Documents'),
                                            ('company_avatar', 'Company Avatar'),
                                            ('company_documents', 'Company Documents'),
                                            ('student_avatar_fallback', 'Student Avatar fallback'),
                                            ('company_avatar_fallback', 'Company Avatar fallback'),
                                            ('challenge_images', 'Challenge images'),
                                            ('challenge_documents', 'Challenge documents'),
                                            ('challenge_fallback', 'Challenge fallback')],
                                   max_length=100),
        ),
        migrations.RenameModel(
            old_name='ProjectType',
            new_name='ChallengeType',
        ),
        migrations.RenameField(
            model_name='challenge',
            old_name='project_from_date',
            new_name='challenge_from_date',
        ),
        migrations.RenameField(
            model_name='challenge',
            old_name='project_type',
            new_name='challenge_type',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='link_projects',
            new_name='link_challenges',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='project_posting',
            new_name='challenge',
        ),
        migrations.AlterField(
            model_name='challenge',
            name='company',
            field=models.ForeignKey(blank=True,
                                    null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='challenges',
                                    to='db.company'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='keywords',
            field=models.ManyToManyField(related_name='challenges', to='db.Keyword'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='student',
            field=models.ForeignKey(blank=True,
                                    null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='challenges',
                                    to='db.student'),
        ),
        migrations.AlterField(
            model_name='onlinechallenge',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='online_challenges',
                                    to='db.student'),
        ),
    ]
