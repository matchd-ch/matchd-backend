from django.db import models
from wagtail.admin.edit_handlers import FieldPanel


class LanguageLevel(models.Model):
    level = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    panels = [
        FieldPanel('level'),
        FieldPanel('description')
    ]

    class Meta:
        ordering = ['level']
