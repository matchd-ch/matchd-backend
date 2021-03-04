from django import forms
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import convert_date, generic_error_dict, validate_student_user_type, validate_step,\
    validate_form_data, convert_object_to_id
from db.models import JobOption, JobPosition, JobOptionMode


class StudentProfileFormStep3(forms.Form):
    job_option = forms.ModelChoiceField(queryset=JobOption.objects.all(), required=True)
    job_position = forms.ModelChoiceField(queryset=JobPosition.objects.all(), required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['job_option'] = convert_object_to_id(data.get('job_option', None))
        data['job_position'] = convert_object_to_id(data.get('job_position', None))
        super().__init__(data=data, **kwargs)


class StudentProfileFormStep3Date(forms.Form):

    def __init__(self, data=None, **kwargs):
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)

    job_from_date = forms.DateField(required=True)


class StudentProfileFormStep3DateRange(forms.Form):

    def __init__(self, data=None, **kwargs):
        data['job_from_date'] = convert_date(data.get('job_from_date', None), '%m.%Y')
        data['job_to_date'] = convert_date(data.get('job_to_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)

    job_from_date = forms.DateField(required=True)
    job_to_date = forms.DateField(required=True)


def process_job_option_form(profile, data):
    errors = {}

    job_option = JobOption.objects.get(pk=profile.job_option.id)

    # we need different forms for different option types
    #
    # JobOptionMode.DATE_RANGE:
    # we need two valid dates and a valid date range (both dates are required)
    #
    # JobOptionMode.DATE_FROM:
    # we need one valid date and need to reset the second date (only one date is required)
    if job_option.mode == JobOptionMode.DATE_RANGE:
        form = StudentProfileFormStep3DateRange(data)
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
    validate_student_user_type(user)
    validate_step(user, 3)
    validate_form_data(data)

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
