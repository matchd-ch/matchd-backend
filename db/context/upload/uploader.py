# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.context.upload.resource import Resource
from db.exceptions import FormException
from db.forms import AttachmentForm
from db.models import Attachment, User, get_attachment_validator_map_for_key
from db.helper import generic_error_dict, validation_error_to_dict
from db.validators import AttachmentKeyValidator, AttachmentKeyNumFilesValidator, AttachmentFileValidator


class Uploader:

    def __init__(self) -> None:
        self.__success = False
        self.__errors = {}

    @staticmethod
    def process_upload(user: User, key: str, files: dict) -> str:
        errors = {}

        profile_content_type = user.get_profile_content_type()
        profile_id = user.get_profile_id()

        # check if a file is uploaded
        # noinspection PyBroadException
        try:
            # when a file is uploaded from the frontend, the file key is '1'
            # when a file is uploaded directly via API, the file key is '0'
            # workaround to use the first file key
            file_key = list(files.keys())[0]
            file = files.get(file_key)
            if file is None:
                errors.update(generic_error_dict('file', _('Field is required'), 'required'))
                raise FormException(errors=errors)
        except Exception:
            errors.update(generic_error_dict('file', _('Field is required'), 'required'))
            # pylint: disable=W0707
            raise FormException(errors=errors)

        errors = {}

        # check if user is allowed to upload files with the provided key
        try:
            validator = AttachmentKeyValidator()
            validator.validate(key, user)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'key'))

        # validate number of attachments for the provided key
        try:
            validator = AttachmentKeyNumFilesValidator()
            validator.validate(key, profile_content_type, profile_id)
        except ValidationError as error:
            errors.update(validation_error_to_dict(error, 'key'))

        if errors:
            raise FormException(errors=errors)

        return file

    @staticmethod
    def process_attachment(user: User, key: str, file: str) -> tuple(str, Attachment):
        errors = {}
        # validate uploaded file and determine the model for the attachment
        validator_model_map = get_attachment_validator_map_for_key(key)

        attachment_model = None
        attachment_model_name = None

        # collect all attachment errors, but return them only if needed
        attachment_errors = {}
        is_valid_attachment = False
        for (model, types, size) in validator_model_map:
            type_failed = False
            # validate file type only
            try:
                validator = AttachmentFileValidator(content_types=types)
                validator.validate(file)
            except ValidationError as error:
                attachment_errors.update(validation_error_to_dict(error, 'file'))
                type_failed = True

            if not type_failed:
                # validate file type and file size
                try:
                    validator = AttachmentFileValidator(max_size=size, content_types=types)
                    validator.validate(file)
                    attachment_model = model
                    # noinspection PyProtectedMember
                    attachment_model_name = model._meta.model_name
                    is_valid_attachment = True
                except ValidationError as error:
                    attachment_errors.update(validation_error_to_dict(error, 'file'))

        if not is_valid_attachment:
            raise FormException(errors=attachment_errors)

        attachment_content_type = ContentType.objects.get(app_label='db',
                                                          model=attachment_model_name)

        # create file attachment (image, video or document)
        try:
            file_attachment = attachment_model.objects.create(file=file, uploaded_by_user=user)
        except attachment_model.DoesNotExist:
            errors.update(generic_error_dict('file', _('File could not be saved.'), 'error'))
            # pylint: disable=W0707
            raise FormException(errors=errors)

        return attachment_content_type, file_attachment

    def upload(self, user: User, resource: Resource) -> Uploader:
        errors = {}
        success = True

        try:
            processed_file = Uploader.process_upload(user, resource.key, resource.file)
            attachment_content_type, file_attachment = Uploader.process_attachment(
                user, resource.key, processed_file)
        except FormException as exception:
            self.__success = False
            self.__errors = exception.errors

            return self

        form = AttachmentForm(
            data={
                'content_type': resource.content_type,
                'object_id': resource.owner,
                'attachment_type': attachment_content_type,
                'attachment_id': file_attachment.id,
                'key': resource.key
            })

        form.full_clean()
        if form.is_valid():
            form.save()
        else:
            success = False
            errors.update(form.errors.get_json_data())

        self.__success = success
        self.__errors = errors

        return self

    @property
    def errors(self) -> list[str]:
        return self.__errors

    @property
    def success(self) -> bool:
        return self.__success
