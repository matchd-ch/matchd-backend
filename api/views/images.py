import imghdr
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from django.views.generic import View
from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError


class ImageServeView(View):
    model = get_image_model()
    action = 'serve'
    key = None

    stacks = settings.IMAGE_STACKS

    @classonlymethod
    def as_view(cls, **initkwargs):
        if 'action' in initkwargs:
            if initkwargs['action'] not in ['serve', 'redirect']:
                raise ImproperlyConfigured("ServeView action must be either 'serve' or 'redirect'")

        return super(ImageServeView, cls).as_view(**initkwargs)

    def get(self, request, image_id, stack, title):
        if stack not in self.stacks:
            raise PermissionDenied

        image = get_object_or_404(self.model, id=image_id)

        try:
            # Get/generate the rendition
            filter_spec = self.stacks.get(stack)
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse("Source image file not found", content_type='text/plain', status=410)
        except InvalidFilterSpecError:
            # noinspection PyUnboundLocalVariable
            return HttpResponse("Invalid filter spec: " + filter_spec, content_type='text/plain', status=400)

        return getattr(self, self.action)(rendition)

    def serve(self, rendition):
        # Open and serve the file
        rendition.file.open('rb')
        image_format = imghdr.what(rendition.file)
        return StreamingHttpResponse(FileWrapper(rendition.file),
                                     content_type='image/' + image_format)

    def redirect(self, rendition):
        # Redirect to the file's public location
        return HttpResponsePermanentRedirect(rendition.url)
