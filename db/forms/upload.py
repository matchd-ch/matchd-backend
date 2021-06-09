from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper import generic_error_dict, validation_error_to_dict
from db.models import get_attachment_validator_map_for_key
from db.validators import AttachmentKeyValidator, AttachmentKeyNumFilesValidator, AttachmentFileValidator


def process_upload(user, key, files):
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


def process_attachment(user, key, file):
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

    attachment_content_type = ContentType.objects.get(app_label='db', model=attachment_model_name)

    # create file attachment (image, video or document)
    try:
        file_attachment = attachment_model.objects.create(file=file, uploaded_by_user=user)
        file_attachment = attachment_model.objects.get(id=file_attachment.id)
    except attachment_model.DoesNotExist:
        errors.update(generic_error_dict('file', _('File could not be saved.'), 'error'))
        raise FormException(errors=errors)

    return attachment_content_type, file_attachment
