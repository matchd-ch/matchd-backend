from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from wagtail.search import index

from db.models.profile_state import ProfileState


def default_date():
    return datetime.strptime('01.01.1970', '%m.%d.%Y').date()


class Student(models.Model, index.Indexed):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='student')
    mobile = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=settings.PHONE_REGEX)])
    street = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=150, null=True, unique=True)
    school_name = models.CharField(blank=True, null=True, max_length=255)
    field_of_study = models.CharField(blank=False, null=False, max_length=255)
    graduation = models.DateField(blank=True, null=True)
    branch = models.ForeignKey('db.Branch', blank=True, null=True, on_delete=models.SET_NULL)
    job_type = models.ForeignKey('db.JobType', blank=True, null=True, on_delete=models.SET_NULL)
    job_from_date = models.DateField(null=True, blank=True)
    job_to_date = models.DateField(null=True, blank=True)
    skills = models.ManyToManyField('db.Skill', related_name='students')
    distinction = models.TextField(max_length=1000, blank=True)
    state = models.CharField(choices=ProfileState.choices, max_length=255, blank=False, default=ProfileState.INCOMPLETE)
    profile_step = models.IntegerField(default=1)
    soft_skills = models.ManyToManyField('db.SoftSkill', blank=True, related_name='students')
    cultural_fits = models.ManyToManyField('db.CulturalFit', blank=True, related_name='students')
    slug = models.CharField(max_length=200, blank=True)

    def get_profile_content_type(self):
        return ContentType.objects.get(app_label='db', model='student')

    def get_profile_id(self):
        return self.id

    @classmethod
    def get_indexed_objects(cls):
        query = Q(state=ProfileState.PUBLIC)
        query |= Q(state=ProfileState.ANONYMOUS)
        return cls.objects.filter(query).prefetch_related('languages', 'languages__language_level',
                                                          'cultural_fits', 'soft_skills', 'skills').\
            select_related('branch', 'job_type')

    search_fields = [
        index.FilterField('branch_id'),
        index.FilterField('job_type_id'),
        index.RelatedFields('cultural_fits', [
            index.FilterField('id'),
        ]),
        index.RelatedFields('soft_skills', [
            index.FilterField('id'),
        ]),
        index.RelatedFields('skills', [
            index.FilterField('id'),
        ]),
        index.FilterField('job_from_date', es_extra={
            'type': 'date',
            'format': 'yyyy-MM-dd',
            'null_value': default_date()
        }),
        index.FilterField('job_to_date', es_extra={
            'type': 'date',
            'format': 'yyyy-MM-dd',
            'null_value': default_date()
        }),
    ]
