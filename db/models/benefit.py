from django.db import models
from wagtail.admin.edit_handlers import FieldPanel


class Benefit(models.Model):
    icon = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel('icon'),
        FieldPanel('name')
    ]

    class Meta:
        ordering = ('name', 'icon',)
