from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from wagtail.images.models import AbstractImage, AbstractRendition
from django.utils.translation import gettext_lazy as _


class Image(AbstractImage):

    # Necessary to resolve related name conflict
    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('uploaded by user'),
        null=True, blank=True, editable=False, on_delete=models.SET_NULL, related_name='+'
    )
    # Necessary to resolve related name conflict
    tags = TaggableManager(help_text=None, blank=True, verbose_name=_('tags'), related_name='image_tags')


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
