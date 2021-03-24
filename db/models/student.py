from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from db.models.profile_state import ProfileState


class Student(models.Model):
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
    job_option = models.ForeignKey('db.JobOption', blank=True, null=True, on_delete=models.SET_NULL)
    job_from_date = models.DateField(null=True, blank=True)
    job_to_date = models.DateField(null=True, blank=True)
    job_position = models.ForeignKey('db.JobPosition', blank=True, null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField('db.Skill', related_name='skills')
    distinction = models.TextField(max_length=1000, blank=True)
    state = models.CharField(choices=ProfileState.choices, max_length=255, blank=False, default=ProfileState.INCOMPLETE)
    profile_step = models.IntegerField(default=1)
    soft_skills = models.ManyToManyField('db.SoftSkill', blank=True, related_name='students')
