from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_step, validate_form_data, validate_company_user_type
from db.models import ProfileType


class UniversityProfileSpecificDataForm(forms.Form):
    description = forms.CharField(max_length=1000, required=False)


def process_university_specific_data_form(user, data):
    # validate user type, step and data
    validate_company_user_type(user, ProfileType.UNIVERSITY)
    validate_step(user, 2)
    validate_form_data(data)
    errors = {}
    company = user.company

    # validate profile data
    form = UniversityProfileSpecificDataForm(data)
    form.full_clean()
    if form.is_valid():
        # update user / profile
        cleaned_data = form.cleaned_data

        company.description = cleaned_data.get('description')
    else:
        errors.update(form.errors.get_json_data())

    if errors:
        raise FormException(errors=errors)

    # update step only if the user has step 2
    if company.profile_step == 2:
        company.profile_step = 3

    # save user / profile
    user.save()
    company.save()
