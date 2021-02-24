import magic
from django.conf import settings
from django.db import models
from django.urls import reverse
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

    mime_type = models.CharField(max_length=100, blank=True, null=True)

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'focal_point_x',
        'focal_point_y',
        'focal_point_width',
        'focal_point_height',
    )

    @property
    def absolute_url(self):
        path = reverse('wagtailimages_serve', args=[self.pk, '--STACK--', self.title])
        path = path.replace('--STACK--', '{stack}')  # Workaround to avoid URL escaping
        return f'{settings.BASE_URL}{path}'

    # noinspection PyBroadException
    def get_mime_type(self):
        if self.mime_type is None:
            try:
                mime = magic.Magic(mime=True)
                self.mime_type = mime.from_file(self.file.path)
            except Exception:
                pass
            self.save(update_fields=['mime_type'])
        return self.mime_type


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
