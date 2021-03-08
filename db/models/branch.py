from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
