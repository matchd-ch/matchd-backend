from wagtail.documents.models import AbstractDocument


class File(AbstractDocument):

    @property
    def absolute_url(self):
        # path = reverse('wagtailimages_serve', args=[self.pk, '--STACK--', self.title])
        # path = path.replace('--STACK--', '{stack}')  # Workaround to avoid URL escaping
        # return f'{settings.BASE_URL}{path}'
        return 'todo'
