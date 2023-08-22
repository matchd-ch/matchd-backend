from django import forms

from db.exceptions import FormException
from db.helper.forms import validate_form_data, validate_company_user_type
from db.models import ProfileType


class UniversityProfileSpecificDataForm(forms.Form):
    description = forms.CharField(max_length=3000, required=False)


def process_university_specific_data_form(user, data):
    # validate user type, data
    validate_company_user_type(user, ProfileType.UNIVERSITY)
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

    # save user / profile
    user.save()
    company.save()
