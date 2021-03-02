import magic
import os
from django.db import models
from wagtail.documents.models import AbstractDocument
from django.utils.translation import gettext_lazy as _


def get_upload_to(instance, filename):
    return instance.get_upload_to(filename)


class File(AbstractDocument):
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_to, verbose_name=_('file'))

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
        return os.path.join(user_type, str(profile_id), 'documents', filename)
