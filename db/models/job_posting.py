from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from wagtail.search import index


def default_date():
    return datetime.strptime('01.01.1970', '%m.%d.%Y').date()


class JobPostingState(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLIC = 'public', _('Public')


# pylint: disable=R0902
class JobPosting(models.Model, index.Indexed):
    title = models.CharField(max_length=50, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=3000)
    job_type = models.ForeignKey('db.JobType',
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE,
                                 related_name='+')
    branches = models.ManyToManyField('db.Branch', related_name='job_postings')
    workload_from = models.IntegerField(blank=False,
                                        null=False,
                                        validators=[MaxValueValidator(100),
                                                    MinValueValidator(10)])
    workload_to = models.IntegerField(blank=False,
                                      null=False,
                                      validators=[MaxValueValidator(100),
                                                  MinValueValidator(10)])
    company = models.ForeignKey('db.Company',
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                related_name='job_postings')
    job_from_date = models.DateField(null=True, blank=True)
    job_to_date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    job_requirements = models.ManyToManyField('db.JobRequirement')
    skills = models.ManyToManyField('db.Skill')
    form_step = models.IntegerField(
        default=2)    # since we save the job posting in step 1 the default value is 2
    state = models.CharField(choices=JobPostingState.choices,
                             default=JobPostingState.DRAFT,
                             max_length=255)
    employee = models.ForeignKey('db.Employee', on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True, blank=True)

    def zip_code(self):
        return None if not self.company.zip else int(self.company.zip)

    def cultural_fits(self):
        return [obj.id for obj in self.company.cultural_fits.all()]

    def soft_skills(self):
        return [obj.id for obj in self.company.soft_skills.all()]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.validate_workload()
        self.validate_work_period()

    @classmethod
    def get_indexed_objects(cls):
        return cls.objects.filter(state=JobPostingState.PUBLIC).select_related('company', 'job_type').\
            prefetch_related('languages', 'languages__language_level', 'skills', 'job_requirements', 'branches')

    search_fields = [
        index.RelatedFields('branches', [
            index.FilterField('id'),
        ]),
        index.FilterField('job_type_id'),
        index.FilterField('workload_from'),
        index.FilterField('workload_to'),
        index.FilterField('job_from_date',
                          es_extra={
                              'type': 'date',
                              'format': 'yyyy-MM-dd',
                              'null_value': default_date()
                          }),
        index.FilterField('job_to_date',
                          es_extra={
                              'type': 'date',
                              'format': 'yyyy-MM-dd',
                              'null_value': default_date()
                          }),
        index.RelatedFields('skills', [
            index.FilterField('id'),
        ]),
        index.FilterField('zip_code'),
        index.FilterField('soft_skills'),
        index.FilterField('cultural_fits'),
    ]

    def validate_workload(self):
        if self.workload_from > self.workload_to:
            raise ValidationError(
                {'workload_to': "Workload to must be greated than workload from."})

    def validate_work_period(self):
        job_from_date = self.job_from_date
        job_to_date = self.job_to_date

        if job_from_date is not None and job_to_date is not None and job_from_date > job_to_date:
            raise ValidationError(
                {'job_to_date': "Job from date to must be greated than job to date."})
