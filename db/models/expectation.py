from django.db import models


class Expectation(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
