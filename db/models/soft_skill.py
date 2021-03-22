from django.db import models


class SoftSkill(models.Model):
    student = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
