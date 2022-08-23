from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_delete
from wagtail.search import index

from .attachment import Attachment
from .profile_type import ProfileType
from .profile_state import ProfileState


class Company(models.Model, index.Indexed):
    # fields for company / university
    type = models.CharField(choices=ProfileType.choices, max_length=255, blank=True)
    state = models.CharField(choices=ProfileState.choices,
                             max_length=255,
                             blank=False,
                             default=ProfileState.INCOMPLETE)
    profile_step = models.IntegerField(default=1)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=255, blank=False)
    street = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=12,
                             blank=True,
                             validators=[RegexValidator(regex=settings.PHONE_REGEX)])
    website = models.URLField(max_length=2048, blank=True)
    branches = models.ManyToManyField('db.Branch', related_name='companies')
    description = models.TextField(max_length=1000, blank=True)

    # fields for company only
    soft_skills = models.ManyToManyField('db.SoftSkill', related_name='companies')
    uid = models.CharField(max_length=255,
                           blank=False,
                           validators=[RegexValidator(regex=settings.UID_REGEX)])
    services = models.TextField(blank=True)
    member_it_st_gallen = models.BooleanField(blank=True, default=False)
    benefits = models.ManyToManyField('db.Benefit', related_name='companies')
    cultural_fits = models.ManyToManyField('db.CulturalFit', related_name='companies')

    # fields for university only
    top_level_organisation_description = models.TextField(max_length=1000, blank=True)
    top_level_organisation_website = models.URLField(max_length=2048, blank=True)
    link_education = models.URLField(max_length=2048, blank=True, null=True)
    link_challenges = models.URLField(max_length=2048, blank=True, null=True)
    link_thesis = models.URLField(max_length=2048, blank=True, null=True)

    def get_profile_content_type(self):
        return ContentType.objects.get(app_label='db', model='company')

    def get_profile_id(self):
        return self.id

    @classmethod
    def get_indexed_objects(cls):
        query = Q(state=ProfileState.PUBLIC)
        query |= Q(state=ProfileState.ANONYMOUS)
        return cls.objects.filter(query).prefetch_related('branches', 'cultural_fits',
                                                          'soft_skills')

    search_fields = [
        index.RelatedFields('branches', [
            index.FilterField('id'),
        ]),
        index.RelatedFields('cultural_fits', [
            index.FilterField('id'),
        ]),
        index.RelatedFields('soft_skills', [
            index.FilterField('id'),
        ])
    ]


class CompanySignalHandler:

    @staticmethod
    def pre_delete(sender, instance, **kwargs):
        pre_delete.disconnect(CompanySignalHandler.pre_delete,
                              Company,
                              dispatch_uid='db.models.CompanySignalHandler.pre_delete')

        # employees
        for user in instance.users.all():
            user.delete()

        # attachments of challenges
        challenge_type = ContentType.objects.get(app_label='db', model='challenge')
        for challenge in instance.challenges.all():
            attachments = Attachment.objects.filter(content_type=challenge_type,
                                                    object_id=challenge.id)
            for attachment in attachments:
                attachment.attachment_object.delete()
            attachments.delete()

        # avatars / moods
        company_type = ContentType.objects.get(app_label='db', model='company')
        attachments = Attachment.objects.filter(content_type=company_type, object_id=instance.id)

        for attachment in attachments:
            attachment.attachment_object.delete()
        attachments.delete()

        pre_delete.connect(CompanySignalHandler.pre_delete,
                           Company,
                           dispatch_uid='db.models.CompanySignalHandler.pre_delete')


pre_delete.connect(CompanySignalHandler.pre_delete,
                   Company,
                   dispatch_uid='db.models.CompanySignalHandler.pre_delete')
