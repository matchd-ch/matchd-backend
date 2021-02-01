from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


class Company(models.Model):
    uid = models.CharField(max_length=255, blank=False,
                           validators=[RegexValidator(regex=r'CHE-[0-9]{3}.[0-9]{3}.[0-9]{3}')])
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
