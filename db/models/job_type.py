from django.db import models
from django.utils.translation import gettext as _


class DateMode(models.TextChoices):
    DATE_FROM = 'date_from', _('Date from')
    DATE_RANGE = 'date_range', _('Date range')


class JobType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    mode = models.CharField(max_length=255, choices=DateMode.choices, null=False, blank=False)

    class Meta:
        ordering = ('name', )
