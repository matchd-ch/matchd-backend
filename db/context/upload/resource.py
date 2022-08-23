from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from db.helper import generic_error_dict
from db.models.attachment import AttachmentKey
from db.models.profile_type import ProfileType
from db.models.challenge import Challenge


class Resource():

    def __init__(self, **kwargs) -> None:
        errors = {}
        is_valid_resource = True
        user = kwargs.get('user')
        key = kwargs.get('key')
        file = kwargs.get('file')
        challenge = kwargs.get('challenge')

        if challenge is not None:
            try:
                challenge = Challenge.objects.get(pk=challenge.get('id'))
            except Challenge.DoesNotExist as exception:
                is_valid_resource = False
                errors = errors.update(generic_error_dict('Challenge', str(exception), 'invalid'))

        if challenge is not None and key not in (
                AttachmentKey.CHALLENGE_DOCUMENTS,
                AttachmentKey.CHALLENGE_IMAGES,
        ):
            is_valid_resource = False
            errors = errors.update(generic_error_dict('key', 'Invalid key', 'invalid'))

        content_type = user.get_profile_content_type()
        resource_owner = user.get_profile_id()

        if challenge is not None:
            if user.type in ProfileType.valid_company_types():
                if user.company != challenge.company:
                    raise PermissionDenied('You are not the owner of this challenge.')
            if user.type in ProfileType.valid_student_types():
                if user.student != challenge.student:
                    raise PermissionDenied('You are not the owner of this challenge.')

            content_type = ContentType.objects.get(app_label='db', model='challenge')
            resource_owner = challenge.id

        self.__errors = errors
        self.__is_valid = is_valid_resource
        self.__key = key
        self.__file = file
        self.__content_type = content_type
        self.__owner = resource_owner

    @property
    def errors(self) -> list[str]:
        return self.__errors

    @property
    def is_valid(self) -> bool:
        return self.__is_valid

    @property
    def file(self) -> dict:
        return self.__file

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def key(self) -> str:
        return self.__key

    @property
    def owner(self) -> int:
        return self.__owner
