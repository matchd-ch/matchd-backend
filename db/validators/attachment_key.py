from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.models import UserType, AttachmentKey


class AttachmentKeyValidator:

    def validate(self, key, user):
        valid = True
        if user.type in UserType.valid_student_types():
            if key not in AttachmentKey.valid_student_keys():
                valid = False
        elif user.type in UserType.valid_company_types():
            if key not in AttachmentKey.valid_company_keys():
                valid = False

        if not valid:
            raise ValidationError(code='invalid_key', message=_('The key you provided is invalid'))
