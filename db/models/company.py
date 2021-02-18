from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


class Company(models.Model):
    uid = models.CharField(max_length=255, blank=False,
                           validators=[RegexValidator(regex=r'CHE-[0-9]{3}.[0-9]{3}.[0-9]{3}')])
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=settings.MOBILE_REGEX)])
    position = models.CharField(max_length=255, blank=True)
