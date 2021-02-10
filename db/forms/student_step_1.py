from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from db.exceptions import FormException
from db.helper import validate_user_type_step_and_data
from db.helper.forms import convert_date


class StudentProfileFormStep1(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    street = forms.CharField(max_length=255, required=False)
    zip = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(required=True)
    mobile = forms.CharField(max_length=12, validators=[RegexValidator(regex=settings.MOBILE_REGEX)], required=False)


def process_student_form_step_1(user, data):
    # validate user type, step and data
    validate_user_type_step_and_data(user, data, 1)

    errors = {}

    # convert date of birth to date
    try:
        data = convert_date(data, 'date_of_birth')
    except FormException as exception:
        errors.update(exception.errors)

    profile = user.student

    # validate profile data
    form = StudentProfileFormStep1(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # required parameters
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        profile.date_of_birth = cleaned_data.get('date_of_birth')

        # optional parameters
        profile.street = cleaned_data.get('street')
        profile.zip = cleaned_data.get('zip')
        profile.city = cleaned_data.get('city')
        profile.mobile = cleaned_data.get('mobile')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 1
    if user.profile_step == 1:
        user.profile_step = 2

    # save user / profile
    user.save()
    profile.save()
