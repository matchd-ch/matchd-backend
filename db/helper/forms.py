from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.models import UserType
from db.validators import ProfileFormStepValidator, StudentTypeValidator, CompanyTypeValidator, \
    JobPostingFormStepValidator


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


def validate_company_user_type(user, sub_type=None):
    errors = {}
    validator = CompanyTypeValidator()
    try:
        validator.validate(user.type)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'type'))

    if sub_type is not None:
        if user.type != sub_type:
            errors.update(generic_error_dict('type', _('Wrong user type'), 'invalid'))

    if errors:
        raise FormException(errors)


def validate_student_user_type(user):
    errors = {}
    validator = StudentTypeValidator()
    try:
        validator.validate(user.type)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'type'))

    if errors:
        raise FormException(errors)


def validate_step(user, step):
    errors = {}

    # validate step
    step_validator = ProfileFormStepValidator(step)
    profile = None
    if user.type in UserType.valid_company_types():
        profile = user.company
    elif user.type in UserType.valid_student_types():
        profile = user.student
    try:
        step_validator.validate(profile)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'profile_step'))

    if errors:
        raise FormException(errors)


def validate_job_posting_step(job_posting, step):
    errors = {}

    # validate step
    step_validator = JobPostingFormStepValidator(step)
    try:
        step_validator.validate(job_posting)
    except ValidationError as error:
        errors.update(validation_error_to_dict(error, 'job_posting_step'))

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
