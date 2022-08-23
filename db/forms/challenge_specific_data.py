from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from db.exceptions import FormException
from db.helper.forms import validate_form_data, convert_date, generic_error_dict
from db.models import Challenge, ProfileType


class ChallengeSpecificDataForm(forms.Form):
    challenge_from_date = forms.DateField(required=False)
    website = forms.URLField(required=False)

    def __init__(self, data=None, **kwargs):
        # due to a bug with ModelChoiceField and graphene_django
        data['challenge_from_date'] = convert_date(data.get('challenge_from_date', None), '%m.%Y')
        super().__init__(data=data, **kwargs)


def process_challenge_specific_data_form(user, data):
    errors = {}

    validate_form_data(data)
    challenge = get_object_or_404(Challenge, id=data.get('id'))
    form = ChallengeSpecificDataForm(data)
    form.full_clean()

    cleaned_data = None

    if form.is_valid():
        cleaned_data = form.cleaned_data
        if user.type in ProfileType.valid_company_types():
            cleaned_data['company'] = user.company
            cleaned_data['employee'] = user.employee
        if user.type in ProfileType.valid_student_types():
            cleaned_data['student'] = user.student
        employee = cleaned_data.get('employee', None)

        # check if employee belongs to the same company as the current user
        if employee is not None:
            if user.type in ProfileType.valid_company_types(
            ) and employee.user.company != user.company:
                errors.update(
                    generic_error_dict('employee', _('Employee does not belong to your company'),
                                       'invalid'))
                raise FormException(errors=errors)

        # check if the challenge belongs to the company
        # ! if the user is a student, both values will be None
        # ! see next if statement
        if user.company != challenge.company:
            errors.update(
                generic_error_dict('employee', _('Challenge does not belong to your company.'),
                                   'invalid'))
            raise FormException(errors=errors)

        # check if the challenge belongs to the student
        if user.type in ProfileType.valid_student_types() and user.student != challenge.student:
            errors.update(
                generic_error_dict('student', _('Challenge does not belong to you.'), 'invalid'))
            raise FormException(errors=errors)
        challenge.employee = employee
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    challenge.challenge_from_date = cleaned_data.get('challenge_from_date')
    challenge.website = cleaned_data.get('website')
    # update job posting
    if challenge.form_step == 2:
        challenge.form_step = 3

    challenge.save()
    return challenge
