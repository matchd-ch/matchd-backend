from django.db import models
from django.utils.translation import gettext as _


class MatchType(models.TextChoices):
    STUDENT = 'student', _('Student')
    JOB_POSTING = 'job_posting', _('Job posting')


class MatchInitiator(models.TextChoices):
    STUDENT = 'student', _('Student')
    COMPANY = 'company', _('Company')


class Match(models.Model):
    student = models.ForeignKey('db.Student', null=False, on_delete=models.CASCADE)
    company = models.ForeignKey('db.Company', null=False, on_delete=models.CASCADE)
    student_confirmed = models.BooleanField(default=False)
    company_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True)
    initiator = models.CharField(choices=MatchInitiator.choices, max_length=100)
    complete = models.BooleanField(default=False)
