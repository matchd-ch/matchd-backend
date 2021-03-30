import magic
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

from db.models import ProfileType, AttachmentKey, get_max_files_for_key, Attachment


@deconstructible
class AttachmentKeyValidator:

    def validate(self, key, user):
        valid = True
        if user.type in ProfileType.valid_student_types():
            if key not in AttachmentKey.valid_student_keys():
                valid = False
        elif user.type in ProfileType.valid_company_types():
            if key not in AttachmentKey.valid_company_keys():
                valid = False

        if not valid:
            raise ValidationError(code='invalid_key', message=_('The key you provided is invalid'))


@deconstructible
class AttachmentKeyNumFilesValidator:

    def validate(self, key, profile_content_type, profile_id):
        max_files_for_key = get_max_files_for_key(key)
        existing_files_for_key = Attachment.objects.filter(key=key, content_type=profile_content_type,
                                                           object_id=profile_id).count()
        if existing_files_for_key >= max_files_for_key:
            raise ValidationError(code='too_many_files', message=_('Too many files for this key'))


@deconstructible
class AttachmentFileValidator:
    def __init__(self, max_size=None, content_types=()):
        self.max_size = max_size
        self.content_types = content_types

    def validate(self, data):
        if self.max_size is not None and data.size > self.max_size:
            max_size = filesizeformat(self.max_size)
            size = filesizeformat(data.size)
            error_message = f'Ensure this file size is not greater than {max_size}. Your file size is {size}.'
            raise ValidationError(error_message, 'max_size')

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                message = f'Files of type {content_type} are not supported'
                raise ValidationError(message, 'content_type')
