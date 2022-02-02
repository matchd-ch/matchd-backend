from django.db import models
from wagtail.admin.edit_handlers import FieldPanel


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_list = models.BooleanField(default=False)

    panels = [FieldPanel('name'), FieldPanel('short_list')]

    class Meta:
        ordering = ['name']
