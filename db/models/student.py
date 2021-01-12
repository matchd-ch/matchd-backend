from django.contrib.auth import get_user_model
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='student')
    mobile_number = models.CharField(max_length=12, blank=False)
