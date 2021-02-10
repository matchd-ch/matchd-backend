from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.models import UserType
from db.validators import StudentProfileFormStepValidator


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
def convert_objects_to_id(data, key, pk_field='id'):
    # convert job option input to integer
    if key in data and data.get(key) is not None and data.get(key).get(pk_field, None) is not None:
        job_option = data.get(key).get(pk_field)
        data[key] = job_option
    else:
        data[key] = None
    return data


# noinspection PyBroadException
def convert_date(data, key, date_format='%d.%m.%Y', required=True):
    errors = {}

    if data.get(key) is None:
        if required:
            errors.update(generic_error_dict(key, _('This field is required.'), 'required'))
        else:
            return data
    else:
        try:
            date = datetime.strptime(data.get(key), date_format).date()
            data[key] = date
        except ValueError as error:
            errors.update(generic_error_dict(key, str(error), 'invalid'))
        except Exception:
            errors.update(generic_error_dict(key, _('Invalid date.'), 'invalid'))

    if errors:
        raise FormException(errors)

    return data


def validate_user_type_step_and_data(user, data, step):
    errors = {}

    # validate user type
    if user.type not in UserType.valid_student_types():
        errors.update(generic_error_dict('type', _('You are not a student'), 'invalid_type'))

    # validate step
    step_validator = StudentProfileFormStepValidator(step)
    try:
        step_validator.validate(user)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'profile_step'))

    # validate profile data
    if data is None:
        errors.update(generic_error_dict('profile_data', _('Missing profile data'), 'required'))

    if errors:
        raise FormException(errors)
