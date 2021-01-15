from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


class Company(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='company')
    uid = models.CharField(max_length=255, blank=False,
                           validators=[RegexValidator(regex=r'CHE-[0-9]{3}.[0-9]{3}.[0-9]{3}')])
    role = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
