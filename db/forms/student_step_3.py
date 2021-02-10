from django import forms
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper import convert_objects_to_id, validate_user_type_step_and_data
from db.helper.forms import convert_date, generic_error_dict
from db.models import JobOption, JobPosition, JobOptionMode


class StudentProfileFormStep3(forms.Form):
    job_option = forms.ModelChoiceField(queryset=JobOption.objects.all(), required=True)
    job_position = forms.ModelChoiceField(queryset=JobPosition.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data = convert_objects_to_id(data, 'job_option')
        data = convert_objects_to_id(data, 'job_position')
        super().__init__(data=data, **kwargs)


class StudentProfileFormStep3Date(forms.Form):
    job_from_date = forms.DateField(required=True)


class StudentProfileFormStep3DateRange(forms.Form):
    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=True)


def process_job_option_form(profile, data):
    errors = {}

    # convert fromDate / toDate
    try:
        data = convert_date(data, 'job_from_date', '%m.%Y')
    except FormException as exception:
        errors.update(exception.errors)

    job_option = JobOption.objects.get(pk=profile.job_option.id)

    # we need different forms for different option types
    #
    # JobOptionTypeChoices.DATE_RANGE:
    # we need two valid dates and a valid date range (both dates are required)
    #
    # JobOptionTypeChoices.DATE_FROM:
    # we need one valid date and need to reset the second date (only one date is required)
    if job_option.mode == JobOptionMode.DATE_RANGE:
        try:
            data = convert_date(data, 'job_to_date', '%m.%Y')
        except FormException as exception:
            errors.update(exception.errors)

        form = StudentProfileFormStep3DateRange(data)
        form.full_clean()
        if form.is_valid():
            # update profile
            cleaned_data = form.cleaned_data

            # validate date range
            from_date = cleaned_data.get('job_from_date')
            to_date = cleaned_data.get('job_to_date')
            if from_date >= to_date:
                errors.update(generic_error_dict('job_to_date', _('Date must be after other date'),
                                                 'invalid_range'))
            else:
                profile.job_from_date = from_date
                profile.job_to_date = to_date
        else:
            errors.update(form.errors.get_json_data())
    else:
        form = StudentProfileFormStep3Date(data)
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


def process_student_form_step_3(user, data):
    errors = {}

    # validate user type, step and data
    validate_user_type_step_and_data(user, data, 3)

    profile = user.student
    form = StudentProfileFormStep3(data)
    form.full_clean()

    if form.is_valid():
        # update user profile
        cleaned_data = form.cleaned_data

        # required parameters
        profile.job_option = cleaned_data.get('job_option')

        # optional parameters
        profile.job_position = cleaned_data.get('job_position')
    else:
        errors.update(form.errors.get_json_data())

    if 'job_from_date' in data and data.get('job_from_date', None) is not None:
        try:
            process_job_option_form(profile, data)
        except FormException as exception:
            errors.update(exception.errors)

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if user.profile_step == 3:
        user.profile_step = 4

    # save user / profile
    user.save()
    profile.save()
