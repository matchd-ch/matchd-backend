from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from db.exceptions import FormException
from db.helper.forms import convert_date, validate_student_user_type, validate_step, validate_form_data


class StudentProfileFormStep1(forms.Form):

    def __init__(self, data=None, **kwargs):
        data['date_of_birth'] = convert_date(data.get('date_of_birth', None))
        super().__init__(data=data, **kwargs)

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    street = forms.CharField(max_length=255, required=False)
    zip = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(required=True)
    mobile = forms.CharField(max_length=12, validators=[RegexValidator(regex=settings.PHONE_REGEX)], required=False)


def process_student_form_step_1(user, data):
    # validate user type, step and data
    validate_student_user_type(user)
    validate_step(user, 1)
    validate_form_data(data)

    errors = {}

    student = user.student

    # validate profile data
    form = StudentProfileFormStep1(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        # required parameters
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        student.date_of_birth = cleaned_data.get('date_of_birth')

        # optional parameters
        student.street = cleaned_data.get('street')
        student.zip = cleaned_data.get('zip')
        student.city = cleaned_data.get('city')
        student.mobile = cleaned_data.get('mobile')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 1
    if student.profile_step == 1:
        student.profile_step = 2

    # save user / profile
    user.save()
    student.save()
