from django.db import models


class Hobby(models.Model):
    name = models.CharField(max_length=255)
