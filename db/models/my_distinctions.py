from django.db import models


class MyDistinctions(models.Model):
    text = models.CharField(max_length=255, unique=True)
