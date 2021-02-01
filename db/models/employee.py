from django.contrib.auth import get_user_model
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='employee')
    company = models.ForeignKey('db.Company', on_delete=models.CASCADE, blank=False, null=False)
    role = models.CharField(max_length=255, blank=False)
