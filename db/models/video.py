from django.db import models
from wagtailmedia.models import AbstractMedia


class Video(AbstractMedia):

    file_size = models.PositiveIntegerField(null=True, editable=False)

    @property
    def absolute_url(self):
        # path = reverse('wagtailimages_serve', args=[self.pk, '--STACK--', self.title])
        # path = path.replace('--STACK--', '{stack}')  # Workaround to avoid URL escaping
        # return f'{settings.BASE_URL}{path}'
        return 'todo'

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
