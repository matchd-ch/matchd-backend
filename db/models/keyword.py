from django.db import models


class Keyword(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        ordering = ('name', )
