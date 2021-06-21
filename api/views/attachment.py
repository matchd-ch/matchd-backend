import imghdr
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError

from db.helper import has_access_to_attachments, get_company_or_student
from db.models import Attachment


class AttachmentServeView(View):
    model = Attachment

    stacks = settings.IMAGE_STACKS
    default_image_stack = 'desktop'

    def get(self, request, attachment_id, stack=None):
        attachment = get_object_or_404(self.model, id=attachment_id)

        user = request.user
        owner = get_company_or_student(attachment.attachment_object.uploaded_by_user)
        if attachment.content_type == ContentType.objects.get(app_label='db', model='projectposting'):
            owner = attachment.content_object
        has_permission = has_access_to_attachments(user, owner, attachment.key)

        if not has_permission:
            raise PermissionDenied

        attachment_content_type = attachment.attachment_type.model
        if attachment_content_type == 'image':
            if stack not in self.stacks:
                stack = self.default_image_stack
            return self.get_image(attachment.attachment_object, stack)
        if attachment_content_type == 'file':
            return self.get_file(attachment.attachment_object)
        if attachment_content_type == 'video':
            return self.get_file(attachment.attachment_object)
        return HttpResponse(status=404)

    def get_file(self, file):
        return StreamingHttpResponse(FileWrapper(file.file), content_type=file.get_mime_type())

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
