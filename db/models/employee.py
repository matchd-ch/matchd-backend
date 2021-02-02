from django.contrib.auth import get_user_model
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='employee')
    role = models.CharField(max_length=255, blank=False)
