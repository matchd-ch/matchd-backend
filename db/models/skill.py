from django.db import models
from wagtail.admin.panels import FieldPanel


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    panels = [FieldPanel('name')]

    class Meta:
        ordering = ['name']
