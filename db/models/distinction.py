from django.db import models


class Distinction(models.Model):
    text = models.CharField(max_length=255)
