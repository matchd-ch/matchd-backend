from django.contrib.auth import get_user_model
from django.db import models

from db.models import Student


class Distinction(models.Model):
    text = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
