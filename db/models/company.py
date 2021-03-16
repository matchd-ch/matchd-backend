from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Company(models.Model):
    uid = models.CharField(max_length=255, blank=False,
                           validators=[RegexValidator(regex=settings.UID_REGEX)])
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
    street = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=12, blank=True, validators=[RegexValidator(regex=settings.PHONE_REGEX)])
    website = models.URLField(max_length=2048, blank=True)
    branch = models.ForeignKey('db.Branch', blank=True, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=1000, blank=True)
    services = models.TextField(blank=True)
    member_it_st_gallen = models.BooleanField(blank=True, default=False)
    benefits = models.ManyToManyField('db.Benefit', related_name='benefits')
    job_positions = models.ManyToManyField('db.JobPosition', related_name='job_positions')
    slug = models.SlugField(unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)
