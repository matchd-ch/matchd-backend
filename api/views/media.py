import imghdr
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.views.generic import View
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError

from db.models import Attachment, Image


class MediaServeView(View):
    model = Attachment

    stacks = settings.IMAGE_STACKS
    default_image_stack = 'desktop'

    def get(self, request, media_id, stack=None):
        if media_id < 1 or media_id > settings.NUMBER_OF_RANDOM_PROFILE_IMAGES:
            return Http404('Image not found')

        if stack not in self.stacks:
            stack = self.default_image_stack

        relative_path = os.path.join('random', f'r-{media_id}.png')
        image = Image.objects.get(file=relative_path)
        return self.get_image(image, stack)

    def get_image(self, image, stack):
        try:
            # Get/generate the rendition
            filter_spec = self.stacks.get(stack)
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse("Source image file not found", content_type='text/plain', status=410)
        except InvalidFilterSpecError:
            # noinspection PyUnboundLocalVariable
            return HttpResponse("Invalid filter spec: " + filter_spec, content_type='text/plain', status=400)

        rendition.file.open('rb')
        image_format = imghdr.what(rendition.file)
        return StreamingHttpResponse(FileWrapper(rendition.file), content_type='image/' + image_format)
