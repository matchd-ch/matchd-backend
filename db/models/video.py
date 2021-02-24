import magic
from django.db import models
from wagtailmedia.models import AbstractMedia


class Video(AbstractMedia):

    file_size = models.PositiveIntegerField(null=True, editable=False)
    mime_type = models.CharField(max_length=100, blank=True, null=True)

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
