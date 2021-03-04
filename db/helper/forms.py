from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.validators import StudentProfileFormStepValidator, StudentTypeValidator, CompanyTypeValidator


def generic_error_dict(key, message, code):
    return {
        key: [
            {
                'message': message,
                'code': code
            }
        ]
    }


def validation_error_to_dict(error, key):
    return generic_error_dict(key, error.message, error.code)


# due to a bug with ModelChoiceField and graphene_django objects needs to be converted to ids
def convert_object_to_id(obj, id_field='id'):
    if obj is None:
        return None
    return obj.get(id_field, None)


# noinspection PyBroadException
def convert_date(date, date_format='%d.%m.%Y'):
    if date is None:
        return None

    try:
        date = datetime.strptime(date, date_format).date()
        return date
    except ValueError:
        pass
    except Exception:
        pass

    return date


def validate_student_type(user):
    errors = {}

    # validate user type
    validator = StudentTypeValidator()
    try:
        validator.validate(user.type)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'type'))

    if errors:
        raise FormException(errors)


def validate_company_type(user):
    errors = {}

    # validate user type
    validator = CompanyTypeValidator()
    try:
        validator.validate(user.type)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'type'))

    if errors:
        raise FormException(errors)


def validate_step(user, step):
    errors = {}

    # validate step
    step_validator = StudentProfileFormStepValidator(step)
    try:
        step_validator.validate(user)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'profile_step'))

    if errors:
        raise FormException(errors)


def validate_form_data(data):
    errors = {}

    # validate profile data
    if data is None:
        errors.update(generic_error_dict('profile_data', _('Missing profile data'), 'required'))

    if errors:
        raise FormException(errors)


def silent_fail(errors):
    if '__all__' in errors:
        if len(errors['__all__']) == 1 and 'code' in errors['__all__'][0]:
            if errors['__all__'][0]['code'] == 'unique_together':
                return True
    return False
