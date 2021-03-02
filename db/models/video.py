import magic
import os
from django.db import models
from wagtailmedia.models import AbstractMedia
from django.utils.translation import gettext_lazy as _


def get_upload_to(instance, filename):
    return instance.get_upload_to(filename)


class Video(AbstractMedia):

    file_size = models.PositiveIntegerField(null=True, editable=False)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_to, verbose_name=_('file'))

    # noinspection PyBroadException
    def get_file_size(self):
        if self.file_size is None:
            try:
                self.file_size = self.file.size
                self.save(update_fields=['file_size'])
            except Exception:
                # silently fail
                pass
        return self.file_size

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

    # noinspection PyUnresolvedReferences
    def get_upload_to(self, filename):
        owner = self.uploaded_by_user
        user_type = owner.get_profile_content_type().name
        profile_id = owner.get_profile_id()
        return os.path.join(user_type, str(profile_id), 'videos', filename)

    def __str__(self):
        return self.title
