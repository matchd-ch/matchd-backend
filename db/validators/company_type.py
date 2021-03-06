from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.models import ProfileType


class CompanyTypeValidator:

    def validate(self, user_type):
        # validate user type
        if user_type not in ProfileType.valid_company_types():
            raise ValidationError(code='invalid_type', message=_('You are not a company'))
