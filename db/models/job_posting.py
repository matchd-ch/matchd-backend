from django.db import models
from django.utils.translation import gettext as _


class JobPostingState(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLIC = 'public', _('Public')


class JobPosting(models.Model):
    description = models.TextField(max_length=1000)
    job_option = models.ForeignKey('db.JobOption', null=False, blank=False, on_delete=models.CASCADE, related_name='+')
    branch = models.ForeignKey('db.Branch', null=False, blank=False, on_delete=models.CASCADE, related_name='+')
    workload = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey('db.Company', null=False, blank=False, on_delete=models.CASCADE)
    job_from_date = models.DateField(null=False, blank=False)
    job_to_date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    expectations = models.ManyToManyField('db.Expectation')
    skills = models.ManyToManyField('db.Skill')
    form_step = models.IntegerField(default=2)  # since we save the job posting in step 1 the default value is 2
    state = models.CharField(choices=JobPostingState.choices, default=JobPostingState.DRAFT, max_length=255)
