from django.db import models


class FAQCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        ordering = ('name', )
