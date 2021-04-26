from django import forms
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import convert_date, generic_error_dict, validate_student_user_type, validate_step,\
    validate_form_data, convert_object_to_id
from db.models import JobType, DateMode, Branch


class StudentProfileFormStep2(forms.Form):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all(), required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['job_type'] = convert_object_to_id(data.get('job_type', None))
        data['branch'] = convert_object_to_id(data.get('branch', None))
        super().__init__(data=data, **kwargs)


class StudentProfileFormStep2Date(forms.Form):

    def __init__(self, data=None, **kwargs):
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)

    job_from_date = forms.DateField(required=True)


class StudentProfileFormStep2DateRange(forms.Form):

    def __init__(self, data=None, **kwargs):
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        data['job_to_date'] = convert_date(data.get('job_to_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)

    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=True)


def process_job_type_form(profile, data):
    errors = {}

    job_type = JobType.objects.get(pk=profile.job_type.id)

    # we need different forms for different option types
    #
    # DateMode.DATE_RANGE:
    # we need two valid dates and a valid date range (both dates are required)
    #
    # DateMode.DATE_FROM:
    # we need one valid date and need to reset the second date (only one date is required)
    if job_type.mode == DateMode.DATE_RANGE:
        form = StudentProfileFormStep2DateRange(data)
        form.full_clean()
        if form.is_valid():
            # update profile
            cleaned_data = form.cleaned_data

            # validate date range
            from_date = cleaned_data.get('job_from_date')
            to_date = cleaned_data.get('job_to_date')
            if from_date >= to_date:
                errors.update(generic_error_dict('job_to_date', _('Date must be after from date'),
                                                 'invalid_range'))
            else:
                profile.job_from_date = from_date
                profile.job_to_date = to_date
        else:
            errors.update(form.errors.get_json_data())
    else:
        form = StudentProfileFormStep2Date(data)
        form.full_clean()
        if form.is_valid():
            # update profile
            cleaned_data = form.cleaned_data
            profile.job_from_date = cleaned_data.get('job_from_date')

            # reset to date
            profile.job_to_date = None
        else:
            errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)


def process_student_form_step_2(user, data):
    errors = {}

    # validate user type, step and data
    validate_student_user_type(user)
    validate_step(user, 2)
    validate_form_data(data)

    student = user.student
    form = StudentProfileFormStep2(data)
    form.full_clean()

    if form.is_valid():
        # update user / profile
        student = user.student
        cleaned_data = form.cleaned_data

        # required parameters
        student.job_type = cleaned_data.get('job_type')

        # optional parameters
        student.branch = cleaned_data.get('branch')
    else:
        errors.update(form.errors.get_json_data())

    # job type can be correct, but if the form is invalid, the student has no
    # job type set
    try:
        job_type = JobType.objects.get(pk=data.get('job_type'))
        student.job_type = job_type
    except JobType.DoesNotExist:
        student.job_type = None

    if student.job_type is not None:
        if 'job_from_date' in data and data.get('job_from_date', None) is not None:
            try:
                process_job_type_form(student, data)
            except FormException as exception:
                errors.update(exception.errors)

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if student.profile_step == 2:
        student.profile_step = 3

    # save user / profile
    user.save()
    student.save()
