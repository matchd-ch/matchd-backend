from django import forms
from django.core.validators import MinLengthValidator

from db.exceptions import FormException
from db.helper import validate_user_type_step_and_data
from db.helper.forms import convert_date


class StudentProfileFormStep2(forms.Form):
    school_name = forms.CharField(max_length=255, required=False)
    field_of_study = forms.CharField(max_length=255, required=False, validators=[MinLengthValidator(3)])
    graduation = forms.DateField(required=False)


def process_student_form_step_2(user, data):
    errors = {}

    # validate user type, step and data
    validate_user_type_step_and_data(user, data, 2)

    # convert graduation to date
    try:
        data = convert_date(data, 'graduation', '%m.%Y', False)
    except FormException as exception:
        errors.update(exception.errors)

    profile = user.student
    form = StudentProfileFormStep2(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        profile = user.student
        cleaned_data = form.cleaned_data

        # optional parameters
        profile.field_of_study = cleaned_data.get('field_of_study')
        profile.school_name = cleaned_data.get('school_name')
        profile.graduation = cleaned_data.get('graduation')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if user.profile_step == 2:
        user.profile_step = 3

    # save user / profile
    user.save()
    profile.save()
