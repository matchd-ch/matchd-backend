from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


class Company(models.Model):
    uid = models.CharField(max_length=255, blank=False,
                           validators=[RegexValidator(regex=settings.UID_REGEX)])
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=settings.MOBILE_REGEX)])
    website = models.URLField(max_length=2048, blank=True)
    branch = models.ForeignKey('db.Branch', blank=True, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=1000, blank=True)
    services = models.TextField(blank=True)
    member_it_st_gallen = models.BooleanField(blank=True, default=False)
