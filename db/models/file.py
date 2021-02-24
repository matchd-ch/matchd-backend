import magic
from django.db import models
from wagtail.documents.models import AbstractDocument


class File(AbstractDocument):
    mime_type = models.CharField(max_length=100, blank=True, null=True)

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
