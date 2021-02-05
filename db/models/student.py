from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='student')
    mobile = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=settings.MOBILE_REGEX)])
    street = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=150, null=True, unique=True)
